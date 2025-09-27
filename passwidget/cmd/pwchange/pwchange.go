package main

import (
	"bufio"
	"io"
	"log"
	"os"
	"strings"

	"github.com/go-crypt/crypt"
	"github.com/go-crypt/crypt/algorithm/scrypt"
)

// Hash the given password and return a digest that can be put in the shadow
// file. All errors are fatal.
func hashPass(pass string) string {
	hasher, err := scrypt.NewYescrypt()
	if err != nil {
		log.Fatalf("failed to init yescrypt hasher: %v", err)
	}

	digest, err := hasher.Hash(pass)
	if err != nil {
		log.Fatalf("failed to hash pass: %v", err)
	}
	// lol. lmao, even
	return digest.Encode()
}

// Replace target's old password with new. Fatally error if any issues arise. Return contents to be put into /etc/shadow.
func lookForAndReplace(target, old, new string) string {
	// Slurp up /etc/shadow into a string and perform modifications there.
	old_shadow, err := os.Open("/etc/shadow")
	if err != nil {
		log.Fatalf("while opening shadow: %v", err)
	}

	var new_shadow_contents string

	old_shadow_reader := bufio.NewReader(old_shadow)
	foundUser := false

	for {
		line, err := old_shadow_reader.ReadString('\n')
		if err == io.EOF {
			break
		} else if err != nil {
			log.Fatalf("while reading shadow: %v", err)
		}

		username, rest, found := strings.Cut(line, ":")
		if !found || username != target {
			new_shadow_contents += line
			continue
		}

		digest, next_rest, found := strings.Cut(rest, ":")
		if !found {
			log.Print("Shadow file missing delim!")
			new_shadow_contents += line
			continue
		}

		valid, err := crypt.CheckPassword(old, digest)
		if err != nil {
			log.Fatalf("While checking password: %v", err)
		}
		if !valid {
			log.Fatalf("Old password didn't match!")
		}

		new_digest := hashPass(new)
		new_shadow_contents += username + ":" + new_digest + ":" + next_rest
		foundUser = true
	}

	if !foundUser {
		log.Fatalf("no user found: %s", target)
	}

	return new_shadow_contents
}

func main() {
	if len(os.Args) != 2 {
		log.Fatalf("Attempt to change password without specifying user.")
	}

	target := os.Args[1]
	log.Printf("Attempting to change password for user: %s", target)

	reader := bufio.NewReader(os.Stdin)
	old_passwd, err := reader.ReadString('\n')
	if err != nil {
		log.Fatalf("while reading old: %v", err)
	}

	new_passwd, err := reader.ReadString('\n')
	if err != nil {
		log.Fatalf("while reading new: %v", err)
	}

	// Remove trailing newline from console input. Note that we shouldn't
	// just trim all leading/trailing whitespace, since a user could
	// possibly start or end their password with whitespace.
	old_passwd = strings.TrimSuffix(old_passwd, "\n")
	new_passwd = strings.TrimSuffix(new_passwd, "\n")

	new_shadow_contents := lookForAndReplace(target, old_passwd, new_passwd)
	// We'll write the output to a new file and then move it over
	// /etc/shadow to keep things as atomic and race-free as possible.
	new_shadow_file, err := os.CreateTemp("", "shadow")
	if err != nil {
		log.Fatalf("can't create new temp shadow file: %v", err)
	}
	defer os.Remove(new_shadow_file.Name())

	new_shadow_bufwr := bufio.NewWriter(new_shadow_file)
	written, err := new_shadow_bufwr.WriteString(new_shadow_contents)
	if written != len(new_shadow_contents) || err != nil {
		log.Fatalf("failed to write to new temp shadow: %v", err)
	}

	if err := os.Rename(new_shadow_file.Name(), "/etc/shadow"); err != nil {
		log.Fatalf("failed to copy over old shadow: %v", err)
	}
}

package main

import (
	_ "embed"
	"errors"
	"html/template"
	"io"
	"log"
	"net/http"
	"os/exec"
	"strings"
)

//go:embed index.html
var rawIndexTempl string

type TemplateData struct {
	Error   string
	Success bool
}

// GET /.
func mkIndex(t *template.Template) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		if err := t.ExecuteTemplate(w, "index", TemplateData{}); err != nil {
			log.Printf("Index failed to exec template: %v", err)
		}
	}
}

func mkUpdate(t *template.Template) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		if err := r.ParseForm(); err != nil {
			log.Printf("ParseForm failed: %v", err)
			w.Header().Set("Content-Type", "text/html; charset=utf-8")
			if err := t.ExecuteTemplate(w, "index", TemplateData{
				Error: "Your browser sent form data that the server couldn't parse. This is a bug. Please email CSTAR.",
			}); err != nil {
				log.Printf("Failed to execute template: %v", err)
			}
			w.WriteHeader(500)
		}

		user := r.Form.Get("user")
		currentPass := r.Form.Get("current")
		newPass := r.Form.Get("new")

		if user == "" || currentPass == "" || newPass == "" {
			if err := t.ExecuteTemplate(w, "index", TemplateData{
				Error: "Username, current password, or new password missing.",
			}); err != nil {
				log.Printf("Failed to execute template: %v", err)
			}
			w.Header().Set("Content-Type", "text/html; charset=utf-8")
			return
		}

		if strings.Contains(currentPass, "\n") || strings.Contains(newPass, "\n") {
			if err := t.ExecuteTemplate(w, "index", TemplateData{
				Error: "Passwords cannot contain newlines. If your current password really does contain a newline, send an email to CSTAR to get a new one.",
			}); err != nil {
				log.Printf("Failed to execute template: %v", err)
			}
		}

		// Try to run pwchange.
		cmd := exec.Command("pwchange", user)

		stdinPipe, err := cmd.StdinPipe()
		if err != nil {
			log.Panicf("Couldn't get stdin pipe: %v", err)
		}

		stderrPipe, err := cmd.StderrPipe()
		if err != nil {
			log.Panicf("Couldn't get stderr pipe: %v", err)
		}

		if err := cmd.Start(); err != nil {
			log.Printf("Can't start pwchange: %v", err)
			t.ExecuteTemplate(w, "index", TemplateData{
				Error: "Internal pwchange tool can't start. Please contact CSTAR.",
			})
			w.WriteHeader(500)
			return
		}

		if _, err := stdinPipe.Write([]byte(currentPass + "\n" + newPass + "\n")); err != nil {
			log.Panicf("Couldn't write to process: %v", err)
		}

		stderrText, err := io.ReadAll(stderrPipe)
		if err != nil {
			log.Panicf("Can't read stderr: %v", err)
		}

		if err := cmd.Wait(); err != nil {
			var exitErr *exec.ExitError
			if errors.As(err, &exitErr) {
				if err := t.ExecuteTemplate(w, "index", TemplateData{
					Error: string(stderrText),
				}); err != nil {
					log.Panicf("Failed to execute template: %v", err)
				}
				return
			} else {
				log.Panicf("Failed to wait on process: %v", err)
			}
		}

		if err := t.ExecuteTemplate(w, "index", TemplateData{
			Success: true,
		}); err != nil {
			log.Printf("Failed to execute template: %v", err)
		}
	}
}

func main() {
	indexTempl, err := template.New("index").Parse(rawIndexTempl)
	if err != nil {
		log.Fatalf("Couldn't parse index template: %v", err)
	}

	http.HandleFunc("GET /pwwidget", mkIndex(indexTempl))
	http.HandleFunc("POST /pwwidget", mkUpdate(indexTempl))

	// Randomly chosen port.
	http.ListenAndServe(":7497", nil)
}

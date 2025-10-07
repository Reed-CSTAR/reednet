# Polytopia

This repository provides a couple things:

### Nix dev shells

These are premade environments that provide all the software used in CS classes. On the CS department machines, you can access them via
```bash
nix develop polytopia#cs221
```

On your own machine (if Nix is installed), you can access them via
```bash
nix develop github:Samasaur1/polytopia#cs384
```

At the time of writing, there are three dev shells:
- cs221
- cs378
- cs384

You can check the dev shells that exist now either by looking in the `devShells` directory or running `nix flake show polytopia`.

##### Upgrades

```bash
nix flake update --commit-lock-file
```

There is a GitHub Action set up that automatically updates the flake inputs weekly, so the only action necessary is to merge this PR.

Perhaps we only want to update dev shells in between semesters, so that they are consistent throughout a class?

### Ansible configuration

There are multiple playbooks provided in `playbooks/` to configure various
aspects of the inventory. They can be run with a command like this:

```bash
ansible-playbook -Kk -u polytopia -i inventory.yaml <path-to-playbook.yaml>
```

##### Adding users

1. Generate a temporary password (let's say it's `correct horse battery staple`)
2. Install `mkpasswd` (you can launch a subshell that provides `mkpasswd` via `nix develop`)
3. Hash the temporary password:

    ```bash
    mkpasswd --method=sha-512
    ```

    If you're using the dev shell:
    ```bash
    poly-hash-password
    ```

    Using our example, this gives `$6$e0A7MR6aAnL3r9Y5$WevmaiUlUo6p67OErBd8.krTCTg/36EnNrpj8zUJKNWwIn3L7MqSmc3rOPupmajxJQ9z3N9Hsg7x9GaZfeVZr.`
4. Add entries to `users/genUserConf.py`
5. Run `genUsersConf.py` and redirect output to `users.yaml`.
5. [Run the Ansible playbook](#running-the-playbook)

## Coder

We run [Coder](https://coder.com/) for reproducible development environments
--- if a class requires that you use CUDA, you can use [our Coder
instance](https://patty.reed.edu:4443/) to access a Docker container running on
Patty.

# GitHub Actions + Docker Compose Demo

A small FastAPI app with automated tests and a Docker image build. GitHub Actions runs CI on GitHub-hosted runners, so Docker does not need to run on your PC for the CI workflow.

## What is included

- `app.py`: FastAPI web app (`/` and `/health`)
- `Dockerfile`: container image definition, runs as a non-root user
- `docker-compose.yml`: local/server Compose configuration
- `tests/`: automated endpoint tests
- `.github/workflows/ci.yml`: runs tests, builds the image, starts a temporary container, and smoke-tests it
- `.github/workflows/deploy-vps.yml`: optional deployment to a VPS you control

## Add these files to GitHub

1. Create or open your GitHub repository.
2. Upload all files in this project, including the hidden `.github` folder and `.dockerignore`.
3. Commit them to the `main` branch.
4. Open the repository's **Actions** tab and select **Docker CI**. It also runs automatically on pushes and pull requests to `main`.

The CI container is temporary: GitHub-hosted runners are removed after the job finishes. This workflow does **not** provide a permanent public website by itself.

## Optional: run permanently on your own VPS

You need a Linux VPS with Docker Engine and the Docker Compose plugin installed, and an SSH account that can run Docker. Keep SSH access restricted and do not expose the Docker daemon to the internet.

For the included `Deploy to VPS (optional)` workflow:

1. Add these repository **Secrets** under **Settings → Secrets and variables → Actions → Secrets**:
   - `VPS_HOST`: public IP or hostname of your VPS
   - `VPS_USER`: SSH username
   - `VPS_SSH_PRIVATE_KEY`: private SSH key for that account
   - `VPS_SSH_PORT`: optional; usually `22`
2. Add these repository **Variables** under **Settings → Secrets and variables → Actions → Variables**:
   - `ENABLE_VPS_DEPLOY` = `true`
   - `REPOSITORY_CLONE_URL` = clone URL the server can access, such as `https://github.com/OWNER/REPOSITORY.git` for a public repository
   - `VPS_APP_DIR` = optional deployment directory, e.g. `/opt/github-actions-docker-demo`
3. If the repository is private, configure read-only access from the VPS to the repository (for example, a deploy key). Do not put tokens or private keys in the repository.
4. Ensure the VPS user's SSH public key is installed in `~/.ssh/authorized_keys`, Docker and the Compose plugin are installed, and the server firewall permits the app port if you want external access.
5. Enable the workflow variable only after the server is configured. Review the workflow and trusted third-party action before use.

The app listens on port `8000`. If the server firewall allows that port, visit `http://YOUR_VPS_IP:8000/`. For a production deployment, use a domain and HTTPS reverse proxy (for example, Caddy or Nginx) rather than exposing a development service directly.

### Important deployment note

The optional VPS workflow executes commands on your server and is intended for a server you control. It does not deploy to GitHub itself. A GitHub repository stores your source and workflows; it is not a permanent Docker host.

## Run locally (optional)

Install Docker Desktop, then from the project directory:

```bash
docker compose up --build -d
```

Visit `http://localhost:8000/` and `http://localhost:8000/health`.

Stop it:

```bash
docker compose down
```

## Security

- Never commit `.env` files, API keys, SSH private keys, or access tokens.
- Protect the `main` branch and review workflow changes before merging.
- For production, pin third-party GitHub Actions to full commit SHAs and use least-privilege credentials.

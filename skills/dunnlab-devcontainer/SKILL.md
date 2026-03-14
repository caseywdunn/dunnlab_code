---
name: dunnlab-devcontainer
description: >
  Add a .devcontainer configuration to a project for secure, reproducible
  Claude Code development environments. Use when setting up devcontainers,
  Docker-based dev environments, or configuring container-based workflows.
---

# Devcontainer Setup

Add a `.devcontainer/` directory to the current project with a production-ready configuration for Claude Code. Based on the [official Claude Code devcontainer](https://code.claude.com/docs/en/devcontainer) and [reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer).

## What to create

Create three files in `.devcontainer/` at the project root:

### 1. `.devcontainer/devcontainer.json`

```json
{
  "name": "Claude Code Sandbox",
  "build": {
    "dockerfile": "Dockerfile",
    "args": {
      "TZ": "${localEnv:TZ:America/Los_Angeles}",
      "CLAUDE_CODE_VERSION": "latest",
      "GIT_DELTA_VERSION": "0.18.2",
      "ZSH_IN_DOCKER_VERSION": "1.2.0"
    }
  },
  "runArgs": [
    "--cap-add=NET_ADMIN",
    "--cap-add=NET_RAW"
  ],
  "customizations": {
    "vscode": {
      "extensions": [
        "anthropic.claude-code",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "eamodio.gitlens"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.codeActionsOnSave": {
          "source.fixAll.eslint": "explicit"
        },
        "terminal.integrated.defaultProfile.linux": "zsh",
        "terminal.integrated.profiles.linux": {
          "bash": {
            "path": "bash",
            "icon": "terminal-bash"
          },
          "zsh": {
            "path": "zsh"
          }
        }
      }
    }
  },
  "remoteUser": "node",
  "mounts": [
    "source=claude-code-bashhistory-${devcontainerId},target=/commandhistory,type=volume",
    "source=claude-code-config-${devcontainerId},target=/home/node/.claude,type=volume"
  ],
  "containerEnv": {
    "NODE_OPTIONS": "--max-old-space-size=4096",
    "CLAUDE_CONFIG_DIR": "/home/node/.claude",
    "POWERLEVEL9K_DISABLE_GITSTATUS": "true"
  },
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=delegated",
  "workspaceFolder": "/workspace",
  "postStartCommand": "sudo /usr/local/bin/init-firewall.sh",
  "waitFor": "postStartCommand"
}
```

### 2. `.devcontainer/Dockerfile`

```dockerfile
FROM node:20

ARG TZ
ENV TZ="$TZ"

# Install basic development tools and iptables/ipset
RUN apt-get update && apt-get install -y --no-install-recommends \
  less \
  git \
  procps \
  sudo \
  fzf \
  zsh \
  man-db \
  unzip \
  gnupg2 \
  gh \
  iptables \
  ipset \
  iproute2 \
  dnsutils \
  aggregate \
  jq \
  nano \
  vim \
  curl \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

ARG USERNAME=node

# Persist bash history.
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
  && mkdir /commandhistory \
  && touch /commandhistory/.bash_history \
  && chown -R $USERNAME /commandhistory

# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true

# Create workspace and config directories and set permissions
RUN mkdir -p /workspace /home/node/.claude && \
  chown -R node:node /workspace /home/node/.claude

WORKDIR /workspace

ARG GIT_DELTA_VERSION=0.18.2
RUN ARCH=$(dpkg --print-architecture) && \
  wget "https://github.com/dandavison/delta/releases/download/${GIT_DELTA_VERSION}/git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb" && \
  sudo dpkg -i "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb" && \
  rm "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb"

# Set up non-root user
USER node

# Set the default shell to zsh rather than sh
ENV SHELL=/bin/zsh

# Set the default editor and visual
ENV EDITOR=nano
ENV VISUAL=nano

# Default powerline10k theme
ARG ZSH_IN_DOCKER_VERSION=1.2.0
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v${ZSH_IN_DOCKER_VERSION}/zsh-in-docker.sh)" -- \
  -p git \
  -p fzf \
  -a "source /usr/share/doc/fzf/examples/key-bindings.zsh" \
  -a "source /usr/share/doc/fzf/examples/completion.zsh" \
  -a "export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
  -x

# Install global packages
ENV NPM_CONFIG_PREFIX=/usr/local/share/npm-global
ENV PATH=$PATH:/usr/local/share/npm-global/bin

# Install Claude Code
ARG CLAUDE_CODE_VERSION=latest
RUN npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}

# Copy and set up firewall script
COPY init-firewall.sh /usr/local/bin/
USER root
RUN chmod +x /usr/local/bin/init-firewall.sh && \
  echo "node ALL=(root) NOPASSWD: /usr/local/bin/init-firewall.sh" > /etc/sudoers.d/node-firewall && \
  chmod 0440 /etc/sudoers.d/node-firewall
USER node
```

### 3. `.devcontainer/init-firewall.sh`

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, and pipeline failures
IFS=$'\n\t'       # Stricter word splitting

# 1. Extract Docker DNS info BEFORE any flushing
DOCKER_DNS_RULES=$(iptables-save -t nat | grep "127\.0\.0\.11" || true)

# Flush existing rules and delete existing ipsets
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
ipset destroy allowed-domains 2>/dev/null || true

# 2. Selectively restore ONLY internal Docker DNS resolution
if [ -n "$DOCKER_DNS_RULES" ]; then
    echo "Restoring Docker DNS rules..."
    iptables -t nat -N DOCKER_OUTPUT 2>/dev/null || true
    iptables -t nat -N DOCKER_POSTROUTING 2>/dev/null || true
    echo "$DOCKER_DNS_RULES" | xargs -L 1 iptables -t nat
else
    echo "No Docker DNS rules to restore"
fi

# First allow DNS and localhost before any restrictions
# Allow outbound DNS
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
# Allow inbound DNS responses
iptables -A INPUT -p udp --sport 53 -j ACCEPT
# Allow outbound SSH
iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT
# Allow inbound SSH responses
iptables -A INPUT -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
# Allow localhost
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Create ipset with CIDR support
ipset create allowed-domains hash:net

# Fetch GitHub meta information and aggregate + add their IP ranges
echo "Fetching GitHub IP ranges..."
gh_ranges=$(curl -s https://api.github.com/meta)
if [ -z "$gh_ranges" ]; then
    echo "ERROR: Failed to fetch GitHub IP ranges"
    exit 1
fi

if ! echo "$gh_ranges" | jq -e '.web and .api and .git' >/dev/null; then
    echo "ERROR: GitHub API response missing required fields"
    exit 1
fi

echo "Processing GitHub IPs..."
while read -r cidr; do
    if [[ ! "$cidr" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$ ]]; then
        echo "ERROR: Invalid CIDR range from GitHub meta: $cidr"
        exit 1
    fi
    echo "Adding GitHub range $cidr"
    ipset add allowed-domains "$cidr" -exist
done < <(echo "$gh_ranges" | jq -r '(.web + .api + .git)[]' | aggregate -q)

# Resolve and add other allowed domains
for domain in \
    "registry.npmjs.org" \
    "api.anthropic.com" \
    "claude.ai" \
    "sentry.io" \
    "statsig.anthropic.com" \
    "statsig.com" \
    "marketplace.visualstudio.com" \
    "vscode.blob.core.windows.net" \
    "update.code.visualstudio.com"; do
    echo "Resolving $domain..."
    ips=$(dig +noall +answer A "$domain" | awk '$4 == "A" {print $5}')
    if [ -z "$ips" ]; then
        echo "ERROR: Failed to resolve $domain"
        exit 1
    fi

    while read -r ip; do
        if [[ ! "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
            echo "ERROR: Invalid IP from DNS for $domain: $ip"
            exit 1
        fi
        echo "Adding $ip for $domain"
        ipset add allowed-domains "$ip" -exist
    done < <(echo "$ips")
done

# Get host IP from default route
HOST_IP=$(ip route | grep default | cut -d" " -f3)
if [ -z "$HOST_IP" ]; then
    echo "ERROR: Failed to detect host IP"
    exit 1
fi

HOST_NETWORK=$(echo "$HOST_IP" | sed "s/\.[0-9]*$/.0\/24/")
echo "Host network detected as: $HOST_NETWORK"

# Set up remaining iptables rules
iptables -A INPUT -s "$HOST_NETWORK" -j ACCEPT
iptables -A OUTPUT -d "$HOST_NETWORK" -j ACCEPT

# Set default policies to DROP first
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# First allow established connections for already approved traffic
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Then allow only specific outbound traffic to allowed domains
iptables -A OUTPUT -m set --match-set allowed-domains dst -j ACCEPT

# Explicitly REJECT all other outbound traffic for immediate feedback
iptables -A OUTPUT -j REJECT --reject-with icmp-admin-prohibited

echo "Firewall configuration complete"
echo "Verifying firewall rules..."
if curl --connect-timeout 5 https://example.com >/dev/null 2>&1; then
    echo "ERROR: Firewall verification failed - was able to reach https://example.com"
    exit 1
else
    echo "Firewall verification passed - unable to reach https://example.com as expected"
fi

# Verify GitHub API access
if ! curl --connect-timeout 5 https://api.github.com/zen >/dev/null 2>&1; then
    echo "ERROR: Firewall verification failed - unable to reach https://api.github.com"
    exit 1
else
    echo "Firewall verification passed - able to reach https://api.github.com as expected"
fi
```

## Test mode

When this skill is invoked with the argument `test`, create a minimal test project to validate the devcontainer configuration and the user's Docker setup. Do NOT apply this to the current project — instead create an isolated test folder.

### Steps

1. Create a temporary test directory at `/tmp/dunnlab-devcontainer-test/`.
2. Scaffold the three `.devcontainer/` files (devcontainer.json, Dockerfile, init-firewall.sh) exactly as specified above into that directory.
3. Initialize a git repo (`git init`) — required for the devcontainer to work.
4. Create a `README.md` with the validation checklist below.
5. Attempt to build the container using the devcontainer CLI: `devcontainer build --workspace-folder /tmp/dunnlab-devcontainer-test`. If the `devcontainer` CLI is not available, report this and include manual instructions instead.
6. If the build succeeds, start the container and run the validation commands listed below. Report results for each check.
7. Clean up: inform the user they can remove the test directory with `rm -rf /tmp/dunnlab-devcontainer-test` when done.

### README.md content for the test project

Write a README.md with this content:

```markdown
# Devcontainer Test

Temporary project to validate the dunnlab-devcontainer configuration.
Created by `/dunnlab-devcontainer test`. Safe to delete after validation.

## How to validate manually

Open this folder in VS Code and run **Dev Containers: Reopen in Container**.
Once the container starts, open a terminal and run these checks:

### 1. Claude Code is installed
    claude --version

### 2. Shell is zsh with powerline theme
    echo $SHELL
    # Expected: /bin/zsh

### 3. Firewall is active (postStartCommand ran)
    sudo iptables -L -n | head -20
    # Should show DROP policies and allowed-domains rules

### 4. Allowed traffic works
    curl -s https://api.github.com/zen
    # Should return a GitHub zen phrase

    curl -s https://api.anthropic.com/ -o /dev/null -w "%{http_code}"
    # Should return a status code (not a connection error)

### 5. Blocked traffic is rejected
    curl --connect-timeout 5 https://example.com
    # Should fail with "Connection refused" or similar

### 6. Git delta is installed
    delta --version

### 7. Workspace permissions
    touch /workspace/test-write && rm /workspace/test-write
    # Should succeed without permission errors

### 8. Node.js is available
    node --version
    # Should show v20.x

## Automated checks

If using `devcontainer exec`, these commands run the same checks non-interactively:

    devcontainer exec --workspace-folder . bash -c "claude --version && echo SHELL=\$SHELL && delta --version && node --version && curl -sf https://api.github.com/zen && ! curl --connect-timeout 5 https://example.com 2>/dev/null && echo ALL_CHECKS_PASSED"
```

### Automated validation commands

When the devcontainer CLI is available, run these checks programmatically after build and report pass/fail for each:

| Check | Command | Pass condition |
|-------|---------|----------------|
| Claude Code installed | `devcontainer exec --workspace-folder /tmp/dunnlab-devcontainer-test claude --version` | Exit code 0 |
| Shell is zsh | `devcontainer exec --workspace-folder /tmp/dunnlab-devcontainer-test bash -c 'echo $SHELL'` | Output contains `/bin/zsh` |
| Node.js available | `devcontainer exec --workspace-folder /tmp/dunnlab-devcontainer-test node --version` | Output starts with `v20` |
| Git delta installed | `devcontainer exec --workspace-folder /tmp/dunnlab-devcontainer-test delta --version` | Exit code 0 |
| Firewall active | `devcontainer exec --workspace-folder /tmp/dunnlab-devcontainer-test sudo iptables -L OUTPUT -n` | Output contains `allowed-domains` |
| Allowed traffic | `devcontainer exec --workspace-folder /tmp/dunnlab-devcontainer-test curl -sf https://api.github.com/zen` | Exit code 0 |
| Blocked traffic | `devcontainer exec --workspace-folder /tmp/dunnlab-devcontainer-test curl --connect-timeout 5 https://example.com` | Exit code non-zero |
| Workspace writable | `devcontainer exec --workspace-folder /tmp/dunnlab-devcontainer-test bash -c 'touch /workspace/t && rm /workspace/t'` | Exit code 0 |

Report a summary table with pass/fail status for each check. If any check fails, include the command output to aid debugging.

## Customization guidance

When adding these files to a project, adapt as needed:

- **Extensions**: Add project-relevant VS Code extensions to `devcontainer.json` (e.g., `ms-python.python` for Python projects, `ms-toolsai.jupyter` for notebooks).
- **Firewall domains**: If the project needs access to additional services (e.g., PyPI, Conda, Docker Hub, cloud APIs), add them to the `init-firewall.sh` domain list.
- **Base image**: For Python-heavy projects, consider switching from `node:20` to a multi-stage build or adding Python/Conda to the Dockerfile.
- **Build args**: Adjust `TZ`, version pins, and other build args for the team's needs.
- **Volumes**: Add additional volume mounts for caching (e.g., conda packages, pip cache) to speed up rebuilds.
- **Multi-architecture support**: The container may run on x86_64 (Linux/Windows hosts) or arm64 (Apple Silicon Macs). When adding software downloads to the Dockerfile, always detect the architecture at build time rather than hardcoding it. Use `dpkg --print-architecture` for `.deb` packages (returns `amd64` or `arm64`) or `uname -m` for installers that use kernel arch names (returns `x86_64` or `aarch64`). For example, to add Miniconda:
  ```dockerfile
  RUN ARCH=$(uname -m) && \
    wget -q "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-${ARCH}.sh" -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    /opt/conda/bin/conda clean -afy
  ENV PATH="/opt/conda/bin:$PATH"
  ```

## Important notes

- The firewall's default-deny policy means `--dangerously-skip-permissions` can be used more safely inside the container, since network access is restricted to whitelisted domains only.
- The `NET_ADMIN` and `NET_RAW` capabilities are required for the firewall to function.
- Docker must be installed on the host machine. Docker Desktop works on macOS and Windows.
- Shell history and Claude configuration persist across container restarts via named volumes.
- Only use devcontainers with trusted repositories — the container does not prevent exfiltration of anything accessible inside it, including Claude Code credentials.

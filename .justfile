# Like GNU `make`, but `just` rustier.
# https://just.systems/
# run `just` from this directory to see available commands

alias i := install
alias p := pre_commit
alias r := run
alias t := tensorboard
alias c := clean

# Default command when 'just' is run without arguments
default:
  @just --list

# Install the virtual environment and pre-commit hooks
install:
  @echo "Installing..."
  @uv sync --refresh
  @uv run pre-commit install --install-hooks

# Run pre-commit
pre_commit:
  @echo "Running pre-commit..."
  @uv run pre-commit run -a
  @find . -name "*.nix" -type f -exec nixfmt {} \;

# Run a package
run package="" *args="":
  @echo "Running..."
  @MUJOCO_GL=egl uv run {{package}} {{args}}

# Run tensorboard
tensorboard logdir="./logs/rsl_rl/":
  @echo "Running tensorboard..."
  @uv run tensorboard --logdir {{logdir}}

# Remove build artifacts and non-essential files
clean:
  @echo "Cleaning..."
  @find . -type d -name ".venv" -exec rm -rf {} +
  @find . -type d -name "__pycache__" -exec rm -rf {} +
  @find . -type d -name "*.ruff_cache" -exec rm -rf {} +
  @find . -type d -name "*.egg-info" -exec rm -rf {} +
  @find . -type d -name "logs" -exec rm -rf {} +
  @find . -type d -name "viser-client" -exec rm -rf {} +
  @find . -type d -name "wandb" -exec rm -rf {} +

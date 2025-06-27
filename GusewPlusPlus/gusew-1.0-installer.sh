#!/bin/bash

echo "🔧 Instalacja Gusew++..."

INSTALL_DIR="$HOME/gusewpp"
REPO_RAW_URL="https://raw.githubusercontent.com/marcinwojewodzki7c/nikitatiuti124unnykfun2032234234/main/GusewPlusPlus/Interpreter.py"

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR" || exit

echo "📥 Pobieram interpreter Interpreter.py..."
curl -fsSL -o gusew "$REPO_RAW_URL"

chmod +x gusew

# Dodaj do PATH, jeśli nie ma
SHELL_RC=""
if [[ $SHELL == */bash ]]; then
  SHELL_RC="$HOME/.bashrc"
elif [[ $SHELL == */zsh ]]; then
  SHELL_RC="$HOME/.zshrc"
fi

if [ -n "$SHELL_RC" ]; then
  if ! grep -q 'gusewpp' "$SHELL_RC"; then
    echo 'export PATH="$HOME/gusewpp:$PATH"' >> "$SHELL_RC"
    echo "✅ Dodano do $SHELL_RC"
    echo "➡️ Uruchom: source $SHELL_RC"
  fi
fi

echo 'a_var "imię" -> "Świat"
say "imię"' > "$INSTALL_DIR/example.gusew"

echo "✅ Instalacja zakończona!"
echo "🟢 Użycie: gusew -krix example.gusew"

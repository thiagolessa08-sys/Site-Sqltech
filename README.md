# Site SQLTECH

Site institucional estático. HTML puro — sem build, sem framework e sem dependência de CDN.

## Publicar no GitHub Pages
1. Envie o conteúdo desta pasta para a raiz do repositório (branch `main`).
2. Settings → Pages → Source: **Deploy from a branch** → `main` / `/ (root)`.
3. O site fica em `https://thiagolessa08-sys.github.io/Site-Sqltech/`.

## Estrutura
- `index.html` — página completa: marcação, CSS e o script de rolagem/animação embutidos
- `assets/hero.png` — imagem do cabeçalho
- `assets/logo-branco.png` — logo da SQLTECH, no topo da página
- `assets/clientes.png` — painel de logos da seção "Quem confia na SQLTECH"
- `.nojekyll` — evita processamento Jekyll

## Editar o conteúdo
Todo o texto está diretamente no `index.html`. Basta abrir o arquivo e alterar.

A cor de destaque do site é a variável CSS `--accent` (`#1668d8`), definida no
bloco `:root` no topo do `<style>` — trocar ali muda o acento do site inteiro.

## Rodar localmente
```
python -m http.server 8000
```
Depois acesse `http://localhost:8000`.

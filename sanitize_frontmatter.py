import os
import yaml

def sanitize_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Si el archivo no comienza con '---', no hay frontmatter problemático
        if not content.startswith('---'):
            return

        lines = content.splitlines()
        if len(lines) < 2:
            return

        end_idx = -1
        # Buscar el cierre del frontmatter (el siguiente '---')
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break

        modified = False
        
        # Caso 1: Frontmatter sin cerrar
        if end_idx == -1:
            lines.pop(0)
            content = '\n'.join(lines)
            modified = True
        else:
            # Caso 2: El bloque no es YAML válido según un parser real
            frontmatter_block = '\n'.join(lines[1:end_idx])
            try:
                parsed = yaml.safe_load(frontmatter_block)
                # Si no es un diccionario (ej. un string vacío o texto sin keys), lo marcamos inválido
                if not isinstance(parsed, dict):
                    raise ValueError("Not a dictionary")
            except Exception:
                # El YAML es inválido (tiene sintaxis Markdown que lo rompe, o no es un diccionario)
                # Eliminamos el primer '---'
                lines.pop(0)
                content = '\n'.join(lines)
                modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[Sanitizado] {filepath}")

    except Exception as e:
        print(f"Error procesando {filepath}: {e}")

def main():
    content_dir = os.path.join(os.getcwd(), 'content')
    if not os.path.exists(content_dir):
        print("El directorio 'content' no existe. Saltando sanitización.")
        return
        
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                sanitize_file(os.path.join(root, file))

if __name__ == '__main__':
    main()

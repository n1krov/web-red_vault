import os

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
            content = '\n' + content
            modified = True
        else:
            # Caso 2: El bloque no tiene formato YAML válido (ej. sin ':' para clave-valor)
            frontmatter_lines = lines[1:end_idx]
            is_valid_yaml = False
            for line in frontmatter_lines:
                if ':' in line:
                    is_valid_yaml = True
                    break
            
            # Si tiene contenido pero no es YAML válido, forzamos que se trate como texto normal
            if not is_valid_yaml and len(frontmatter_lines) > 0:
                content = '\n' + content
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

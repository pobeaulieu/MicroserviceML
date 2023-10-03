

## Formattage du code source

`src_code/pos/com` contient le code source original

`src_code/pos/source_code_formatted` contient toutes les classes, avec le nom modifié pour contenir tous le path, séparé  par des .

Pour ce faire, executer ces commandes une à la suite de l'autre (fonctionne sur mac)

Cela permet d'améliorer le setup initial de Imen, dans lequel il fallait modifier le nom des classes avec le meme nom manuellement. Maintenant, le nom des classe est le path complet pour éviter cette situation.  

Note: pas besoin d'exécuter ces commandes si le dossier `src_code/pos/source_code_formatted` es déjà rempli.

- `cd src_code/pos` 
- `find . -name "*.java" -exec bash -c 'dest="./src_code_formatted/${1//\//.}"; mkdir -p "$(dirname "$dest")"; cp {} "$dest"' _ {} \;`
- `find src_code_formatted -type f -execdir bash -c 'mv "$1" "${1#..}"' bash {} \;`



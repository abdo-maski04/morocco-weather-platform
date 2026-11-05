import logging as log
import src
import src.quality as quality

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
) # sert à configurer le logger pour afficher les messages de log avec un format spécifique, incluant l'heure, le niveau de log et le message.


quality.run_quality_checks()
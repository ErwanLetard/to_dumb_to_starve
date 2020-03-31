# to_dumb_to_starve

Génération d'une population sur une map (class Individu et class Map)
Chaque individu a un jauge de vie, une espérance de vie, une jauge d'aggressivité (à compléter)

 - La jauge de vie diminue de 1 à chaque pas de temps (c'est sa faim, quand elle arrive à zéro il meurt)
 - L'espérance de vie dépend des ancêtres de l'individu, elle est calculé une fois à la naissance et l'individu en a conscience (devient plus aggressif en fin de vie, possibilité de l'augmenter avec certaine action?)
 - une jauge d'aggressivité qui determine les rapports "sociaux" de chaque individu. Plus il est aggressif plus il a de chance d'attaquer un voisin.
 
 Il faut trouver un moyen astucieux de générer les nouvelles générations. On peut lancer sur un certain temps, garder les "gènes" des survivants, générer une nouvelle population basée sur ces "gènes" + des déviations random. 
 Ou alors on essaie de faire en sorte qu'il y ait un incentive à ce que les individus se reproduisent et transmettent leur gènes (genre en fin de vie, ils ne pensent plus qu'à baiser ou quelque chose comme ça) 
 
 Vu que j'ai pas encore étudié TensorFlow j'ai pas d'idée bien précise de ce qui est faisable ou non. Mais je pense que ce que j'ai décrit ici l'est.

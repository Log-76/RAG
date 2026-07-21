# RAG

Rag
La génération augmentée de récupération ou RAG (Retrieval-Augmented Generation) est une technique qui améliore la qualité et la pertinence des réponses fournies par une application d'IA générative

le but:
La RAG permet au LLM de présenter des informations précises avec l'attribution de la source. Le résultat peut inclure des citations ou des références à des sources. Les utilisateurs peuvent également rechercher eux-mêmes les documents sources s'ils ont besoin de précisions ou de détails supplémentaires.

[*video*](https://www.youtube.com/watch?v=S-LUZ4vrkIQ)

Flux de données d'un système RAG:
![Flux de données d'un système RAG](flux_RAG.png)

Comme le montre le schéma ci-dessus, le système repose sur l'interaction entre deux blocs principaux :

Le Retriever (L'archiviste) : 

	Il prend tes documents, les découpe en morceaux (Document chunks), les transforme en vecteurs (nombres) via un Embedding model et les stocke dans une base de données vectorielle (Vector DB). Quand l'utilisateur pose une question, le Retriever cherche les morceaux de texte les plus pertinents.

Le Generator (Le rédacteur) : 

	Il prend la question de l'utilisateur + les morceaux de texte trouvés par l'archiviste (le Context), donne le tout à un modèle de langage (Pre-trained LLM), qui rédige enfin une réponse précise.
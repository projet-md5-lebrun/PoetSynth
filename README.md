# Générateur de Poèmes

Ce projet a pour objectif de créer un générateur automatique de poèmes en utilisant un modèle de langage issu d'une fondation. Contrairement à l'approche traditionnelle basée sur les LSTM, nous avons opté pour l'utilisation d'un modèle de langage pré-entraîné provenant d'une fondation pour plusieurs raisons.

**Avantages du modèle linguistique de base**

**Performances**

Les LLM sont généralement plus performants que les réseaux de neurones récurrents pour les tâches de traitement du langage naturel, ici la GenAI. Cela est dû au fait que les LLM sont capables d'apprendre des relations entre les mots à long terme, ce qui est essentiel pour ces tâches.

**Puissance de calcul**

Les LLM nécessitent moins de puissance de calcul que les réseaux de neurones récurrents pour être entraînés. Cela est dû au fait que les LLM sont capables de traiter les séquences de texte en une seule fois, tandis que les réseaux de neurones récurrents doivent traiter les séquences de texte un caractère à la fois.

**Facilité d'entraînement**

Les LLM sont plus faciles à entraîner que les réseaux de neurones récurrents. Cela est dû au fait que les LLM sont capables d'apprendre des relations entre les mots à long terme sans avoir besoin de mécanismes complexes tels que les portes de mémoire. 'Memory gates'



**Inconvénients des réseaux de neurones récurrents**

**Capacité d'apprentissage des séquences longues**

Les réseaux de neurones récurrents sont limités dans leur capacité à apprendre des séquences longues. Cela est dû au fait que les réseaux de neurones récurrents doivent traiter les séquences de texte un caractère à la fois, ce qui peut entraîner une perte d'information.

**Coût de calcul**

Les réseaux de neurones récurrents nécessitent plus de puissance de calcul que les LLM pour être entraînés. Cela est dû au fait que les réseaux de neurones récurrents doivent traiter les séquences de texte un caractère à la fois, ce qui peut entraîner une accumulation d'erreurs.

**Difficulté d'entraînement**

Les réseaux de neurones récurrents sont plus difficiles à entraîner que les LLM. Cela est dû au fait que les réseaux de neurones récurrents doivent apprendre des relations entre les mots à long terme, ce qui peut entraîner des problèmes de divergence.

**Coût du compute**

L'entraînement d'un modèle linguistique de base nécessite une grande quantité de puissance de calcul. Cependant, les coûts du compute ont considérablement diminué ces dernières années. En 2023, il est possible d'entraîner un modèle linguistique de base sur un cloud computing à un coût abordable.

**Sources**

* Google Cloud Platform: [https://cloud.google.com/](https://cloud.google.com/)
* Amazon Web Services: [https://aws.amazon.com/](https://aws.amazon.com/)
* Microsoft Azure: [https://azure.microsoft.com/en-us/](https://azure.microsoft.com/en-us/)

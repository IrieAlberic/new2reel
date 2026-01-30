# News2Reel
> *Transformez vos textes en vidéos virales en quelques secondes. Open source, modulaire et conçu pour les créateurs.*

News2Reel est un moteur d'automatisation de contenu qui transforme un sujet, une URL ou une idée en une vidéo courte soignée (Reel/TikTok/Short). L'application gère l'intégralité du processus : rédaction du script, synthèse vocale, génération d'images et montage vidéo.

Nous avons créé cet outil car nous croyons que **la création de contenu de haute qualité doit être accessible à tous**, sans abonnements mensuels coûteux.

## Pourquoi News2Reel ?
- **Moteur IA Hybride** : Mélangez les fournisseurs. Utilisez des outils gratuits (Pollinations, EdgeTTS, Gemini) pour un coût nul, ou passez aux API premium (OpenAI DALL-E 3, GPT-4) pour une qualité studio.
- **Architecture Modulaire** : Vous voulez changer le rédacteur ? Le modèle de voix ? Le code est conçu avec des interfaces claires (`ScriptGenerator`, `AudioGenerator`) pour faciliter l'intégration de nouveaux outils.
- **Interface Premium** : Une interface moderne en "Glassmorphism" construite sur Streamlit, offrant l'expérience d'une application professionnelle.
- **Confidentialité Locale** : Votre historique et vos analyses restent sur votre machine (`data/database.json`), pas dans notre cloud.

## Mises à jour récentes
- **Formats Intelligents** : Génère automatiquement du contenu en 9:16 (Shorts) ou 16:9 (YouTube).
- **Effet Ken Burns** : Les images statiques prennent vie avec des animations de zoom et de panoramique subtiles.
- **Mixage Audio** : La musique de fond s'adapte automatiquement à la voix off.
- **Scraping Direct** : Collez une URL et laissez l'IA la résumer en un script vidéo.

## Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-username/news2reel.git
   cd news2reel
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
   *Note : L'installation de `imagemagick` peut être nécessaire sur Linux/Mac pour MoviePy.*

3. **Lancer l'application**
   ```bash
   streamlit run app.py
   ```

## Feuille de route : Nos prochaines étapes
Ce n'est que le début. Voici ce que nous prévoyons de construire, et votre aide est la bienvenue :

- [ ] **Sous-titres Intégrés** : Incrustation automatique des sous-titres dans la vidéo.
- [ ] **Transitions Avancées** : Passages plus fluides entre les clips.
- [ ] **Vidéo-vers-Vidéo** : Utilisation de générateurs vidéo AI (Runway/Luma) au lieu d'images statiques.
- [ ] **Publication en un clic** : Upload direct vers YouTube/TikTok depuis l'application.

## Contribuer au projet
Ce projet est open source et s'enrichit grâce à la communauté.

- **Un bug ?** Ouvrez une issue.
- **Une idée ?** Forkez le dépôt et proposez une Pull Request.
- **Discuter ?** Contactez-nous ou lancez une discussion.

Construisons ensemble l'avenir de l'automatisation de contenu.

---
*Développé par Iriea*

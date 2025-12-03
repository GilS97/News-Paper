# 🤖 Smart Robot Car - Application Android

Application Android moderne et élégante pour contrôler votre Robot Car via Bluetooth.

## 📱 Fonctionnalités

### 🎮 6 Modes de Contrôle

1. **Remote Control**
   - Contrôle manuel avec joystick virtuel
   - Mode capteur de gravité (gyroscope)
   - Contrôle de vitesse dynamique (0-100)
   - Rotation gauche/droite

2. **Line Tracking**
   - Suivi automatique de ligne noire
   - Mode autonome avec capteurs infrarouges

3. **Avoid Obstacles**
   - Évitement automatique d'obstacles
   - Utilisation des capteurs ultrasoniques
   - Navigation autonome intelligente

4. **IR Remote**
   - Contrôle via télécommande infrarouge
   - Compatible avec la télécommande fournie

5. **Light Seeking**
   - Recherche automatique de sources lumineuses
   - Mode autonome avec photorésistances

6. **Follow Me**
   - Le robot vous suit automatiquement
   - Détection ultrasonique de distance

## 🛠️ Technologies Utilisées

- **Langage**: Java
- **Architecture**: MVVM (Model-View-ViewModel)
- **UI**: Material Design 3
- **Navigation**: Navigation Component
- **Connectivité**: Bluetooth Classic (SPP)
- **Capteurs**: Accéléromètre (Gravity Sensor)

## 📋 Prérequis

- Android 7.0 (API 24) ou supérieur
- Bluetooth activé
- Module Bluetooth HC-05/HC-06 sur le robot
- Code Arduino compatible (fourni)

## 🚀 Installation

### Option 1: Ouvrir dans Android Studio

1. Clonez ou téléchargez ce projet
2. Ouvrez Android Studio
3. Sélectionnez "Open an Existing Project"
4. Naviguez vers le dossier `smart-robot-car-app`
5. Attendez la synchronisation Gradle
6. Connectez votre appareil Android ou lancez un émulateur
7. Cliquez sur "Run" (▶️)

### Option 2: Compiler via ligne de commande

```bash
cd smart-robot-car-app
./gradlew assembleDebug
# L'APK sera dans: app/build/outputs/apk/debug/
```

## 📡 Configuration Bluetooth

### Étape 1: Appairer le Robot

1. Activez le Bluetooth sur votre téléphone/tablette
2. Recherchez l'appareil "HC-05" ou "HC-06" dans les paramètres Bluetooth
3. Appairez l'appareil (code PIN par défaut: `1234` ou `0000`)

### Étape 2: Connexion dans l'Application

1. Lancez l'application Smart Robot Car
2. Appuyez sur l'icône Bluetooth en haut à droite
3. Sélectionnez votre robot dans la liste
4. Attendez le message "Bluetooth Connected"
5. L'icône devient verte quand la connexion est établie

## 🎯 Utilisation

### Mode Remote Control

1. Appuyez sur la carte "Remote Control"
2. **Joystick**: Faites glisser votre doigt pour contrôler la direction
3. **Gravity Sensor**: Activez le switch pour contrôler par inclinaison
4. **Vitesse**: Utilisez les boutons + et - pour ajuster
5. **Rotation**: Utilisez les boutons ⟲ et ⟳ pour tourner sur place

### Modes Autonomes

Pour les modes Line Tracking, Avoid Obstacles, IR Remote, Light Seeking et Follow Me:

1. Appuyez sur la carte du mode souhaité
2. Le robot démarre automatiquement en mode autonome
3. Appuyez sur "STOP" pour arrêter le mode
4. Utilisez le bouton retour pour revenir au menu

## 🔧 Protocole de Communication

L'application utilise le protocole série suivant:

| Commande | Description |
|----------|-------------|
| `%G#` | Active le mode Gyroscope/Remote Control |
| `%T#` | Active le mode Line Tracking |
| `%A#` | Active le mode Avoid Obstacles |
| `%I#` | Active le mode IR Remote |
| `%P#` | Active le mode Light Seeking (Phototaxis) |
| `%F#` | Active le mode Follow Me |
| `%Q` | Arrête le mode actuel |
| `%S` | Arrête le mouvement |
| `%L` | Rotation gauche |
| `%R` | Rotation droite |
| `@[angle]#` | Envoie l'angle (-180 à 180) en mode Gyroscope |
| `%[speed]+` | Définit la vitesse (0-100) |

## 🎨 Design

### Thème

- **Couleur principale**: Bleu foncé (#1E3A5F)
- **Accent**: Orange (#FF9F43) et Jaune (#FFC107)
- **Mode**: Dark theme par défaut
- **Style**: Material Design 3 avec glassmorphism

### Animations

- Transitions fluides entre écrans
- Effets de ripple sur les cartes
- Animations d'apparition/disparition
- Feedback visuel sur les interactions

## 📱 Permissions

L'application demande les permissions suivantes:

- ✅ `BLUETOOTH` - Communication Bluetooth basique
- ✅ `BLUETOOTH_ADMIN` - Gestion des connexions
- ✅ `BLUETOOTH_CONNECT` (Android 12+) - Connexion aux appareils
- ✅ `BLUETOOTH_SCAN` (Android 12+) - Scan des appareils
- ✅ `ACCESS_FINE_LOCATION` - Requise pour Bluetooth scan (Android < 12)

## 🔍 Troubleshooting

### Le Bluetooth ne se connecte pas

1. Vérifiez que le module Bluetooth du robot est alimenté (LED clignotante)
2. Assurez-vous que l'appareil est appairé dans les paramètres Android
3. Redémarrez le robot et réessayez
4. Vérifiez que le code Arduino est correctement chargé

### Le Joystick ne répond pas

1. Vérifiez que le mode Gravity Sensor n'est pas activé
2. Assurez-vous que le Bluetooth est connecté
3. Redémarrez l'application

### Le mode Gravity Sensor ne fonctionne pas

1. Vérifiez que votre appareil possède un accéléromètre
2. Désactivez la rotation automatique de l'écran
3. Calibrez votre appareil en le maintenant à plat

## 🏗️ Structure du Projet

```
smart-robot-car-app/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/robotcar/smart/
│   │   │   │   ├── MainActivity.java
│   │   │   │   ├── bluetooth/
│   │   │   │   │   ├── BluetoothManager.java
│   │   │   │   │   └── BluetoothViewModel.java
│   │   │   │   ├── ui/
│   │   │   │   │   ├── home/HomeFragment.java
│   │   │   │   │   ├── remotecontrol/RemoteControlFragment.java
│   │   │   │   │   ├── linetracking/LineTrackingFragment.java
│   │   │   │   │   ├── avoidobstacles/AvoidObstaclesFragment.java
│   │   │   │   │   ├── irremote/IRRemoteFragment.java
│   │   │   │   │   ├── lightseeking/LightSeekingFragment.java
│   │   │   │   │   └── followme/FollowMeFragment.java
│   │   │   │   ├── utils/CommandProtocol.java
│   │   │   │   └── views/JoystickView.java
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   ├── values/
│   │   │   │   ├── navigation/
│   │   │   │   └── anim/
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle
│   └── proguard-rules.pro
├── build.gradle
├── settings.gradle
└── README.md
```

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence MIT.

## 👨‍💻 Auteur

Développé avec ❤️ pour le pilotage du Smart Robot Car

## 🔗 Liens Utiles

- [Documentation Android](https://developer.android.com/)
- [Material Design](https://material.io/design)
- [Bluetooth Android](https://developer.android.com/guide/topics/connectivity/bluetooth)

---

**Version**: 1.0.0
**Dernière mise à jour**: Décembre 2025

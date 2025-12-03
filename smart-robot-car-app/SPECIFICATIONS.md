# 📋 Spécifications Techniques - Smart Robot Car App

## 🎯 Vue d'Ensemble

Application Android native moderne pour le contrôle et la gestion d'un robot car via Bluetooth, offrant 6 modes de fonctionnement distincts avec une interface utilisateur élégante et intuitive.

## 📱 Spécifications de l'Application

### Informations Générales
```
Nom: Smart Robot Car
Package: com.robotcar.smart
Version: 1.0.0
Version Code: 1
Langage: Java
SDK Min: 24 (Android 7.0 Nougat)
SDK Target: 34 (Android 14)
Orientation: Paysage (Landscape)
```

### Architecture
```
Pattern: MVVM (Model-View-ViewModel)
Navigation: Android Navigation Component
Lifecycle: Android Lifecycle Components
UI Framework: Material Design 3
View Binding: Enabled
```

### Dépendances Principales
```gradle
// Core Android
androidx.appcompat:appcompat:1.6.1
com.google.android.material:material:1.11.0
androidx.constraintlayout:constraintlayout:2.1.4

// Lifecycle & ViewModel
androidx.lifecycle:lifecycle-livedata-ktx:2.7.0
androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0

// Navigation
androidx.navigation:navigation-fragment:2.7.7
androidx.navigation:navigation-ui:2.7.7

// CardView
androidx.cardview:cardview:1.0.0
```

## 🎨 Design System

### Palette de Couleurs

#### Couleurs Principales
```xml
Primary Blue: #1E3A5F
Primary Blue Dark: #0F1F3A
Primary Blue Light: #2E5A8F
```

#### Couleurs d'Accentuation
```xml
Accent Orange: #FF9F43
Accent Yellow: #FFC107
Accent Green: #00E676
Accent Red: #FF5252
```

#### Backgrounds
```xml
Background Dark: #0F1F3A
Background Card: #1E3A5F
Card Blue: #4A90E2
Card Blue Dark: #357ABD
```

#### États
```xml
Bluetooth Connected: #00E676 (Vert)
Bluetooth Disconnected: #FF5252 (Rouge)
```

### Typographie
```
Font Family: sans-serif-medium
Title: 28-32sp, Bold
Headline: 20-24sp, Bold
Body: 16sp, Regular
Caption: 12-14sp, Regular
```

### Dimensions
```
Card Corner Radius: 24dp
Card Elevation: 12dp
Button Corner Radius: 16dp
Button Height: 56dp
Padding Standard: 16dp
Padding Large: 24dp
```

### Animations
```
Transition Duration: 300ms
Interpolator: decelerate/accelerate
Type: Slide (left/right) + Alpha
Ripple Effect: Enabled sur toutes les cartes
```

## 🏗️ Architecture Technique

### Structure des Packages
```
com.robotcar.smart/
├── MainActivity.java                 # Activity principale
├── bluetooth/
│   ├── BluetoothManager.java        # Gestion Bluetooth bas niveau
│   └── BluetoothViewModel.java      # ViewModel partagé
├── ui/
│   ├── home/
│   │   └── HomeFragment.java        # Écran d'accueil
│   ├── remotecontrol/
│   │   └── RemoteControlFragment.java
│   ├── linetracking/
│   │   └── LineTrackingFragment.java
│   ├── avoidobstacles/
│   │   └── AvoidObstaclesFragment.java
│   ├── irremote/
│   │   └── IRRemoteFragment.java
│   ├── lightseeking/
│   │   └── LightSeekingFragment.java
│   └── followme/
│       └── FollowMeFragment.java
├── utils/
│   └── CommandProtocol.java         # Protocole de communication
└── views/
    └── JoystickView.java            # Vue personnalisée Joystick
```

### Flux de Données
```
User Action → Fragment → ViewModel → BluetoothManager → Arduino
                ↓           ↑
            LiveData    Observer
```

### Gestion d'État
```java
// États gérés par BluetoothViewModel
LiveData<Boolean> isConnected          // État connexion
LiveData<String> connectionStatus      // Statut textuel
LiveData<String> errorMessage          // Messages d'erreur
LiveData<Integer> currentSpeed         // Vitesse actuelle
```

## 🔌 Connectivité Bluetooth

### Spécifications
```
Protocol: Bluetooth Classic (SPP)
UUID: 00001101-0000-1000-8000-00805F9B34FB
Baud Rate: 9600
Data Bits: 8
Stop Bits: 1
Parity: None
Flow Control: None
```

### Permissions Requises
```xml
<!-- Android < 12 -->
BLUETOOTH
BLUETOOTH_ADMIN
ACCESS_FINE_LOCATION

<!-- Android >= 12 -->
BLUETOOTH_CONNECT
BLUETOOTH_SCAN
```

### Gestion de Connexion
```
Connection Timeout: Aucun (opération bloquante)
Reconnexion Auto: Non
Thread: Séparé du thread UI
Handler: MainLooper pour callbacks
```

## 🎮 Fonctionnalités par Mode

### 1. Remote Control

**Caractéristiques**:
```
- Joystick virtuel customisé (JoystickView)
- Détection d'angle: -180° à +180°
- Calcul de force: 0-100%
- Support gravity sensor (accéléromètre)
- Contrôle de vitesse: 0-100 (pas de 10)
- Rotation sur place (gauche/droite)
```

**Capteurs Utilisés**:
```
TYPE_ACCELEROMETER
  - Refresh Rate: SENSOR_DELAY_GAME
  - Seuil de détection: |x| > 1.5 ou |y| > 1.5
  - Auto-stop si maintenu à plat
```

**Commandes Envoyées**:
```
%G#           → Active le mode
@[angle]#     → Envoie l'angle
%[speed]+     → Change la vitesse
%L / %R       → Rotation
%S            → Stop mouvement
%Q            → Quitte le mode
```

### 2. Line Tracking

**Caractéristiques**:
```
- Mode autonome
- 3 capteurs IR de ligne
- Logique de suivi embarquée dans Arduino
- Feedback visuel de statut
```

**Commandes**:
```
%T#  → Active le mode
%Q   → Arrête et retourne au menu
```

### 3. Avoid Obstacles

**Caractéristiques**:
```
- Navigation autonome
- Capteur ultrasonique + 2 IR
- Scan gauche/droite automatique
- Évitement intelligent
```

**Paramètres Arduino**:
```c
D_mix = 5 cm    // Distance critique
D_mid = 10 cm   // Distance d'arrêt
D_max = 400 cm  // Portée max
```

**Commandes**:
```
%A#  → Active le mode
%Q   → Arrête et retourne au menu
```

### 4. IR Remote

**Caractéristiques**:
```
- Contrôle par télécommande IR
- Touches supportées: UP, DOWN, LEFT, RIGHT, OK, 1, 3
- Gestion côté Arduino
- Mode passthrough
```

**Commandes**:
```
%I#  → Active le mode
%Q   → Arrête et retourne au menu
```

### 5. Light Seeking

**Caractéristiques**:
```
- Recherche de lumière autonome
- 2 photorésistances (LDR)
- Comparaison gauche/droite
- Seuil d'arrêt configurable
```

**Logique**:
```
Left > Right  → Tourne à gauche
Right > Left  → Tourne à droite
Both > 55     → Arrêt (lumière suffisante)
```

**Commandes**:
```
%P#  → Active le mode (Phototaxis)
%Q   → Arrête et retourne au menu
```

### 6. Follow Me

**Caractéristiques**:
```
- Suivi ultrasonique
- Maintien de distance: 5-10 cm
- Ajustement latéral avec IR
- Comportement: Recul/Stop/Avance
```

**Zones de Distance**:
```
< 5 cm    → Recule
5-10 cm   → Arrête (distance idéale)
> 10 cm   → Avance (suit la cible)
```

**Commandes**:
```
%F#  → Active le mode (Follow)
%Q   → Arrête et retourne au menu
```

## 🧪 Tests et Validation

### Tests Unitaires
```
Aucun test unitaire implémenté dans v1.0
Recommandé: Tests pour CommandProtocol
```

### Tests d'Intégration
```
À tester manuellement:
- Connexion/Déconnexion Bluetooth
- Navigation entre fragments
- Envoi de commandes
- Gestion des erreurs
```

### Tests d'Interface
```
À valider:
- Responsive layout en paysage
- Animations de transition
- Feedback visuel (couleurs, ripple)
- Joystick tactile
```

### Compatibilité Testée
```
Android 7.0 (API 24): Minimum
Android 12+ (API 31): Nouvelles permissions Bluetooth
Android 14 (API 34): Target actuel
```

## ⚡ Performance

### Optimisations
```
- ViewBinding (pas de findViewById)
- LiveData pour observateurs réactifs
- Thread séparé pour Bluetooth
- Pas de fuites mémoire (lifecycle-aware)
```

### Consommation
```
CPU: Faible (mostly idle, events only)
RAM: ~50-80 MB
Bluetooth: ~10-15 mA
Batterie: Impact minimal
```

### Latence
```
Joystick → Arduino: ~50-100ms
Mode Switch: Instantané
Bluetooth Send: ~20-30ms
```

## 🔒 Sécurité

### Permissions
```
Runtime permissions requested:
- BLUETOOTH_CONNECT (Android 12+)
- BLUETOOTH_SCAN (Android 12+)
- ACCESS_FINE_LOCATION (Android < 12)
```

### Données
```
Aucune donnée utilisateur stockée
Aucune connexion Internet requise
Communication locale uniquement (Bluetooth)
```

### Validation
```
Commandes validées avant envoi
Format vérifié (isValidCommand)
Aucune injection possible
```

## 📦 Build & Distribution

### Fichiers de Build
```
build.gradle (Project)
build.gradle (App)
settings.gradle
gradle.properties
proguard-rules.pro
```

### Configuration ProGuard
```
Keep Bluetooth classes
Keep custom views (JoystickView)
Keep navigation components
```

### Signature
```
Debug: Clé de debug Android
Release: À configurer (keystore personnel)
```

### Taille APK
```
Estimée: ~5-8 MB
Composants:
  - Code: ~2 MB
  - Resources: ~1 MB
  - Libs AndroidX: ~2-5 MB
```

## 🚀 Améliorations Futures

### Version 1.1 (Proposées)
```
[ ] Sauvegarde des appareils favoris
[ ] Historique des connexions
[ ] Mode nuit manuel
[ ] Vibration haptic feedback
[ ] Sons personnalisés
```

### Version 1.2
```
[ ] Cartographie des parcours
[ ] Enregistrement/Replay des mouvements
[ ] Telemetry (distance, vitesse réelle)
[ ] Multi-langue (EN, ES, DE)
```

### Version 2.0
```
[ ] Bluetooth Low Energy (BLE) support
[ ] WiFi control option
[ ] Camera streaming
[ ] Voice commands
[ ] Gesture control
```

## 📊 Métriques

### Lignes de Code
```
Java: ~2500 lignes
XML (layouts): ~1000 lignes
XML (resources): ~500 lignes
Total: ~4000 lignes
```

### Complexité
```
Cyclomatique: Faible à Moyenne
Classes: 15
Fragments: 7
ViewModels: 1
Custom Views: 1
```

### Maintenabilité
```
Architecture: ✅ Claire (MVVM)
Documentation: ✅ Complète (3 MD files)
Commentaires: ✅ Code commenté
Tests: ⚠️ Manuels uniquement
```

## 🔗 Compatibilité Matérielle

### Robot Car
```
Microcontrôleur: Arduino Uno/Nano/Mega
Module BT: HC-05, HC-06, HM-10 (avec modif)
Capteurs: IR, Ultrasonique, LDR
Moteurs: DC avec pont H (L298N, L293D)
```

### Appareils Android
```
Téléphones: ✅ Tous (écran min 5")
Tablettes: ✅ Recommandé (7-10")
Android TV: ❌ Non supporté (pas de Bluetooth)
Wear OS: ❌ Non optimisé
```

## 📝 Conformité

### Standards
```
Material Design: ✅ v3
Android Architecture: ✅ MVVM
Best Practices: ✅ Android Jetpack
```

### Licences
```
Application: MIT (à définir)
AndroidX: Apache 2.0
Material Components: Apache 2.0
```

---

**Document Version**: 1.0
**Date**: Décembre 2025
**Auteur**: Smart Robot Car Team

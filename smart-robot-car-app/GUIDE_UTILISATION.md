# 📱 Guide d'Utilisation - Smart Robot Car

Guide complet en français pour utiliser l'application de pilotage du Robot Car.

## 🚀 Démarrage Rapide

### 1. Préparation du Robot

1. **Vérifiez le matériel**
   - Robot complètement assemblé
   - Batteries chargées (généralement 4 piles AA ou batterie Li-ion)
   - Module Bluetooth HC-05/HC-06 correctement connecté
   - Code Arduino chargé sur la carte

2. **Allumez le robot**
   - Mettez l'interrupteur sur ON
   - La LED du module Bluetooth doit clignoter rapidement (non connecté)
   - Le robot émet un bip sonore au démarrage (si buzzer installé)

### 2. Installation de l'Application

#### Option A: Via Android Studio (Développeurs)
```bash
1. Ouvrez le projet dans Android Studio
2. Connectez votre appareil Android (mode développeur activé)
3. Cliquez sur Run ▶️
4. L'application s'installe automatiquement
```

#### Option B: Installation APK (Utilisateurs)
```bash
1. Copiez le fichier APK sur votre appareil
2. Activez "Sources inconnues" dans les paramètres
3. Ouvrez le fichier APK
4. Appuyez sur "Installer"
5. Lancez l'application
```

### 3. Première Connexion

1. **Appairage Bluetooth**
   ```
   Paramètres Android → Bluetooth → Rechercher
   → Sélectionnez "HC-05" ou "HC-06"
   → Entrez le code PIN: 1234 (ou 0000)
   ```

2. **Connexion dans l'application**
   ```
   Lancez Smart Robot Car
   → Appuyez sur l'icône Bluetooth (coin supérieur droit)
   → Sélectionnez votre robot
   → Attendez "Bluetooth Connected"
   ```

## 🎮 Modes de Contrôle Détaillés

### Mode 1: Remote Control (Contrôle à Distance)

**Utilisation**: Pilotage manuel du robot

#### Contrôles Disponibles

1. **Joystick Virtuel**
   - Placez votre doigt au centre du joystick
   - Déplacez-le dans la direction souhaitée
   - Plus vous éloignez du centre, plus la vitesse augmente
   - Relâchez pour arrêter

2. **Mode Capteur de Gravité**
   - Activez le switch "Gravity Sensor"
   - Inclinez votre tablette/téléphone
   - Avant/Arrière: Avancer/Reculer
   - Gauche/Droite: Tourner
   - Maintenez à plat pour arrêter

3. **Contrôle de Vitesse**
   - Bouton **+**: Augmente de 10 (max 100)
   - Bouton **−**: Diminue de 10 (min 0)
   - Vitesse affichée en grand au centre
   - Barre de progression visuelle

4. **Rotation sur Place**
   - Bouton **⟲**: Rotation gauche
   - Bouton **⟳**: Rotation droite
   - Utile pour ajuster l'orientation

#### Conseils d'Utilisation
```
✓ Commencez avec une vitesse de 60 pour les tests
✓ Augmentez progressivement selon le terrain
✓ En mode gravité, maintenez l'écran en paysage
✓ Évitez les mouvements brusques
```

### Mode 2: Line Tracking (Suivi de Ligne)

**Utilisation**: Le robot suit automatiquement une ligne noire

#### Préparation
1. Tracez une ligne noire sur fond blanc (3-5 cm de largeur)
2. Utilisez du ruban adhésif électrique noir
3. Évitez les virages trop serrés (rayon min: 20 cm)

#### Fonctionnement
```
1. Appuyez sur "Line Tracking"
2. Placez le robot sur la ligne (capteurs centrés)
3. Le robot démarre automatiquement
4. Il suit la ligne jusqu'à ce que vous appuyiez sur STOP
```

#### Dépannage
- **Robot sort de la ligne**: Vérifiez les capteurs infrarouges
- **Virage raté**: Réduisez la vitesse dans le code Arduino
- **S'arrête subitement**: Ligne interrompue détectée

### Mode 3: Avoid Obstacles (Évitement d'Obstacles)

**Utilisation**: Navigation autonome avec évitement

#### Comment ça marche
```
1. Appuyez sur "Ultrasound Avoid Obstacles"
2. Placez le robot dans un espace dégagé
3. Le robot explore son environnement
4. Il évite automatiquement les obstacles
```

#### Comportement du Robot
- **Rien devant**: Avance tout droit
- **Obstacle proche**: Arrêt et scan gauche/droite
- **Obstacle très proche**: Recule puis scan
- **Meilleur chemin trouvé**: Tourne et continue

#### Portée des Capteurs
```
Distance minimale: 5 cm
Distance d'arrêt: 10 cm
Portée maximale: 4 mètres
Angle de détection: ~15°
```

### Mode 4: IR Remote (Télécommande Infrarouge)

**Utilisation**: Contrôle via la télécommande IR fournie

#### Touches Supportées
```
▲ (UP): Avancer
▼ (DOWN): Reculer
◄ (LEFT): Tourner à gauche (progressif)
► (RIGHT): Tourner à droite (progressif)
OK: Arrêter
1: Rotation gauche sur place
3: Rotation droite sur place
```

#### Configuration
1. Appuyez sur "IR Remote" dans l'app
2. Pointez la télécommande vers le capteur IR du robot
3. Appuyez sur les touches pour contrôler
4. Maintenez la pression pour actions continues

#### Remarques
- Portée: 5-8 mètres
- Ligne de vue directe requise
- Évitez la lumière directe du soleil

### Mode 5: Light Seeking (Recherche de Lumière)

**Utilisation**: Le robot cherche et se dirige vers la lumière

#### Mise en Place
```
1. Appuyez sur "Light Seeking"
2. Placez le robot dans une zone peu éclairée
3. Positionnez une source lumineuse (lampe, téléphone)
4. Le robot se dirige automatiquement vers la lumière
```

#### Sources Lumineuses Recommandées
- ✅ Lampe de poche
- ✅ Lampe de bureau
- ✅ Écran de téléphone (luminosité max)
- ❌ Évitez: Soleil direct (sature les capteurs)

#### Fonctionnement
```
Photorésistance Gauche > Droite → Tourne à gauche
Photorésistance Droite > Gauche → Tourne à droite
Lumière équilibrée → Avance tout droit
Lumière très forte → S'arrête (objectif atteint)
```

### Mode 6: Follow Me (Suivi Ultrasonique)

**Utilisation**: Le robot vous suit automatiquement

#### Utilisation Optimale
```
1. Appuyez sur "Follow Me"
2. Tenez-vous devant le robot (face aux capteurs)
3. Distance optimale: 10-20 cm
4. Déplacez-vous lentement
5. Le robot maintient la distance
```

#### Zones de Distance
```
< 5 cm: Robot recule (trop proche)
5-10 cm: Robot s'arrête (distance parfaite)
> 10 cm: Robot avance (vous suit)
```

#### Astuces
- Portez des vêtements clairs (meilleure détection)
- Évitez les mouvements latéraux brusques
- Maintenez votre main devant le capteur
- Utilisez dans un couloir pour de meilleurs résultats

## ⚙️ Paramètres et Réglages

### Ajuster la Vitesse par Défaut
Dans le code Arduino:
```c
void setup() {
    BLE_Change_SPEED = 60;  // Changez cette valeur (0-100)
}
```

### Sensibilité des Capteurs
```c
// Suivi de ligne - seuil noir/blanc
int Black = 1;
int white = 0;

// Évitement d'obstacles - distances
D_mix = 5;   // Distance minimale (cm)
D_mid = 10;  // Distance d'arrêt (cm)
D_max = 400; // Portée maximale (cm)
```

### Calibration des Photorésistances
```c
void Light_Seeking() {
    Left_photosensitive = analogRead(A0) / 10;
    Right_photosensitive = analogRead(A3) / 10;

    // Ajustez le seuil d'arrêt
    if (Left_photosensitive > 55 && Right_photosensitive > 55) {
        // Arrêt (valeur modifiable)
    }
}
```

## 🔧 Dépannage

### Problème: Bluetooth ne se connecte pas

**Solutions**:
1. ✅ Vérifiez que le robot est allumé
2. ✅ LED Bluetooth clignote rapidement
3. ✅ Appairage effectué dans paramètres Android
4. ✅ Redémarrez le robot et l'application
5. ✅ Vérifiez la distance (< 10 mètres)

### Problème: Robot ne répond pas aux commandes

**Solutions**:
1. Vérifiez la connexion Bluetooth (icône verte)
2. Arrêtez le mode actuel (bouton STOP)
3. Redémarrez le mode
4. Vérifiez les piles/batterie
5. Rechargez le code Arduino

### Problème: Mouvements saccadés

**Causes possibles**:
- Piles faibles → Remplacez les piles
- Moteurs encrassés → Nettoyez
- Vitesse trop élevée → Réduisez à 40-60
- Interférences Bluetooth → Rapprochez-vous

### Problème: Capteurs ne détectent pas

**Line Tracking**:
- Nettoyez les capteurs IR avec un chiffon
- Vérifiez le contraste ligne/fond
- Ajustez la hauteur des capteurs (5-10 mm du sol)

**Ultrasonic**:
- Vérifiez les connexions Echo/Trigger
- Testez avec Serial Monitor: `Serial.println(distance)`
- Surface réfléchissante recommandée

**Photorésistances**:
- Testez avec Serial Monitor: `Serial.println(Left_photosensitive)`
- Valeurs normales: 0-100
- Si bloqué à 0 ou 100 → Capteur défectueux

## 📊 Indicateurs de l'Application

### Icône Bluetooth
```
🔴 Rouge: Déconnecté
🟢 Vert: Connecté
```

### États de Connexion
```
"bluetooth is not connected": En attente
"Bluetooth Connected": Connecté et prêt
"Disconnected": Connexion perdue
"Error": Erreur de communication
```

### Indicateur de Vitesse
```
0-30: Lent (exploration)
40-60: Normal (utilisation courante)
70-90: Rapide (surfaces lisses)
91-100: Maximum (utilisation prudente)
```

## 🎯 Conseils d'Utilisation Avancés

### Optimiser la Batterie
```
- Utilisez des piles rechargeables de qualité
- Vitesse 60 = autonomie optimale
- Modes autonomes consomment plus (scan constant)
- Arrêtez les modes quand inutilisés
```

### Meilleures Performances
```
✓ Sol lisse: Parquet, carrelage
✓ Éclairage normal: Intérieur, pas de soleil direct
✓ Espace dégagé: Min 2x2 mètres pour modes autonomes
✓ Distance Bluetooth: < 5 mètres pour stabilité
```

### Sécurité
```
⚠ Ne laissez pas le robot tomber d'une table
⚠ Évitez l'eau et l'humidité
⚠ Ne forcez pas les moteurs bloqués
⚠ Éteignez après utilisation
```

## 📞 Support

### Ressources
- README.md: Documentation technique
- PROTOCOL.md: Protocole de communication
- Code Arduino fourni: Commenté en détail

### Problèmes Courants
Consultez la section Troubleshooting du README.md

---

**Bon pilotage avec votre Smart Robot Car! 🤖🎮**

**Version**: 1.0.0
**Dernière mise à jour**: Décembre 2025

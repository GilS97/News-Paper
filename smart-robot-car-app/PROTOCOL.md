# 📡 Protocole de Communication Bluetooth

Documentation détaillée du protocole de communication entre l'application Android et le Robot Car Arduino.

## 🔌 Configuration Matérielle

### Module Bluetooth
- **Type**: HC-05 ou HC-06
- **Baud Rate**: 9600
- **UUID**: 00001101-0000-1000-8000-00805F9B34FB (SPP)
- **Mode**: Slave

### Connexion Arduino
```
HC-05 VCC  -> Arduino 5V
HC-05 GND  -> Arduino GND
HC-05 TX   -> Arduino RX (Serial)
HC-05 RX   -> Arduino TX (Serial)
```

## 📨 Format des Commandes

Toutes les commandes sont envoyées en ASCII via le port série à 9600 bauds.

### Structure Générale
```
[PREFIX][DATA][SUFFIX]
```

- **PREFIX**: Caractère de début (`%` ou `@`)
- **DATA**: Données de la commande
- **SUFFIX**: Caractère de fin (`#` optionnel)

## 🎮 Commandes de Mode

### Activation des Modes

| Commande | Mode | Description |
|----------|------|-------------|
| `%G#` | Gyroscope/Drive | Active le mode pilotage manuel avec gyroscope |
| `%T#` | Line Tracking | Active le suivi de ligne infrarouge |
| `%A#` | Avoidance | Active l'évitement d'obstacles ultrasonique |
| `%I#` | IR Remote | Active le contrôle par télécommande IR |
| `%P#` | Phototaxis | Active la recherche de lumière |
| `%F#` | Follow | Active le mode suivi ultrasonique |

### Arrêt

| Commande | Description |
|----------|-------------|
| `%Q` | Arrête le mode actuel et retourne en idle |
| `%S` | Arrête le mouvement immédiatement |

## 🕹️ Commandes de Mouvement (Mode Gyroscope)

### Angle de Direction

**Format**: `@[ANGLE]#`

**Paramètres**:
- `ANGLE`: Entier de -180 à 180
  - `0°`: Avant
  - `90°`: Droite
  - `-90°` ou `270°`: Gauche
  - `180°` ou `-180°`: Arrière

**Exemples**:
```
@0#      -> Avancer tout droit
@45#     -> Avancer en tournant vers la droite
@-45#    -> Avancer en tournant vers la gauche
@90#     -> Tourner à droite sur place
@180#    -> Reculer
```

### Calcul de Vitesse des Moteurs

Le code Arduino calcule les vitesses des moteurs gauche et droit selon l'angle:

```c
// Pour 0° <= angle <= 90°
vitesse_gauche = vitesse_base
vitesse_droite = vitesse_base * (angle / 90)

// Pour 90° < angle <= 180°
vitesse_gauche = vitesse_base * ((180 - angle) / 90)
vitesse_droite = vitesse_base

// Pour -180° < angle <= -90°
vitesse_gauche = vitesse_base * ((angle + 180) / 90)
vitesse_droite = vitesse_base

// Pour -90° < angle < 0°
vitesse_gauche = vitesse_base
vitesse_droite = vitesse_base * ((angle + 90) / 90)
```

## ⚡ Contrôle de Vitesse

### Définir la Vitesse

**Format**: `%[SPEED][OPERATOR]`

**Paramètres**:
- `SPEED`: Entier de 0 à 100
- `OPERATOR`: `+` pour incrémenter, `-` pour décrémenter

**Exemples**:
```
%60+     -> Définit la vitesse à 60
%80+     -> Définit la vitesse à 80
%40-     -> Définit la vitesse à 40
```

**Note**: L'opérateur `+` ou `-` est utilisé dans le code Arduino pour différencier les commandes, mais les deux définissent directement la vitesse.

## 🔄 Commandes de Rotation

| Commande | Description | Action |
|----------|-------------|--------|
| `%L` | Rotation gauche | Moteur gauche recule, moteur droit avance |
| `%R` | Rotation droite | Moteur gauche avance, moteur droit recule |

Ces commandes sont utilisées pour les rotations sur place.

## 🤖 Comportement des Modes Autonomes

### Mode Line Tracking (`%T#`)
```
État: En attente de la commande %Q pour arrêter
Capteurs: 3 capteurs infrarouges de suivi de ligne
Logique:
  - Si ligne au centre: Avancer
  - Si ligne à gauche: Tourner à gauche
  - Si ligne à droite: Tourner à droite
  - Si pas de ligne: Arrêter
```

### Mode Avoid Obstacles (`%A#`)
```
État: Navigation autonome avec évitement
Capteurs: Ultrasonique (avant), 2 infrarouges (gauche/droite)
Distances:
  - D_mix: 5 cm (distance minimale)
  - D_mid: 10 cm (distance médiane)
  - D_max: 400 cm (distance maximale)
Logique:
  - Si obstacle < D_mid: Scanner gauche/droite et tourner
  - Si obstacle < D_mix: Reculer puis scanner
  - Sinon: Avancer
```

### Mode Follow (`%F#`)
```
État: Suivi de cible
Capteurs: Ultrasonique + 2 infrarouges
Zones:
  - Distance < 5 cm: Reculer
  - 5-10 cm: Arrêter (distance optimale)
  - Distance > 10 cm: Avancer
Ajustements latéraux avec infrarouges
```

### Mode Light Seeking (`%P#`)
```
État: Recherche de lumière
Capteurs: 2 photorésistances (gauche/droite)
Logique:
  - Compare les valeurs gauche/droite
  - Tourne vers la source la plus lumineuse
  - Arrête si lumière suffisante (> 55)
```

### Mode IR Remote (`%I#`)
```
État: En attente de commandes IR
Capteur: Récepteur infrarouge
Télécommande supportée:
  - UP: Avancer
  - DOWN: Reculer
  - LEFT: Tourner gauche
  - RIGHT: Tourner droite
  - OK: Arrêter
  - 1: Rotation gauche
  - 3: Rotation droite
```

## 🔧 Mapping des Broches Arduino

### Moteurs
```c
Pin 2 (dir_a): Direction moteur A (HIGH = avant, LOW = arrière)
Pin 4 (dir_b): Direction moteur B (HIGH = avant, LOW = arrière)
Pin 5 (pwm_a): PWM vitesse moteur A (0-255)
Pin 6 (pwm_b): PWM vitesse moteur B (0-255)
```

### Capteurs
```c
// Ultrasonique
Pin 12: Trigger
Pin 13: Echo

// Infrarouges obstacles
Pin A1: Capteur gauche
Pin A2: Capteur droit

// Suivi de ligne
Pin 7: Capteur gauche
Pin 8: Capteur centre
Pin 9: Capteur droit

// Photorésistances
Pin A0: Gauche
Pin A3: Droite

// IR Remote
Pin 3: Récepteur IR

// Servo ultrasonique
Pin 10: Servo (balayage gauche/droite)
```

## 📊 Exemples de Séquences

### Démarrage Remote Control
```
Android -> Arduino: %G#
Arduino: Active le mode gyroscope
Android -> Arduino: %60+
Arduino: Définit la vitesse à 60
Android -> Arduino: @45#
Arduino: Avance en tournant à droite
Android -> Arduino: %Q
Arduino: Arrête le mode et le mouvement
```

### Démarrage Line Tracking
```
Android -> Arduino: %T#
Arduino: Active le suivi de ligne
(Le robot suit la ligne automatiquement)
Android -> Arduino: %Q
Arduino: Arrête le mode
```

### Changement de Vitesse en Mouvement
```
Android -> Arduino: %G#
Arduino: Mode gyroscope activé
Android -> Arduino: %50+
Android -> Arduino: @0#
Arduino: Avance à vitesse 50
Android -> Arduino: %80+
Arduino: Augmente la vitesse à 80
Android -> Arduino: @90#
Arduino: Tourne à droite à vitesse 80
```

## ⚠️ Notes Importantes

1. **Délai entre commandes**: Le code Arduino attend 2ms entre chaque caractère (`delay(2)`)
2. **Buffer série**: Le code Arduino lit tous les caractères disponibles avant de traiter
3. **Priorité d'arrêt**: La commande `%Q` est vérifiée dans toutes les boucles de mode
4. **Timeout**: Aucun timeout n'est implémenté, les modes tournent indéfiniment jusqu'à `%Q`
5. **Validation**: Le code vérifie les formats `%X#` pour les modes et `@X#` pour les angles

## 🐛 Debugging

### Activer les logs Arduino
```c
Serial.begin(9600);
Serial.println(BLE_value);  // Déjà présent dans le code
```

### Commandes de test via Serial Monitor
```
%G#     // Test mode gyroscope
%60+    // Test vitesse
@0#     // Test avancer
@90#    // Test droite
%Q      // Test arrêt
```

### Vérification connexion Bluetooth
1. LED du module HC-05 clignote rapidement = Non connecté
2. LED clignote lentement (2 sec) = Connecté
3. Vérifier le pairing dans les paramètres Android
4. Tester avec une application Bluetooth Terminal générique

## 🔄 Diagramme de Flux

```
[Démarrage]
    ↓
[Attente commande]
    ↓
[Reçoit %X#] → [Active mode X] → [Boucle mode]
    │                                 │
    │                                 ↓
    │                        [Reçoit commandes]
    │                                 │
    │                                 ↓
    │                          [Reçoit %Q?]
    │                           Oui ↓  Non
    │                              ↓    ↑
    └──────────────────────────────┘    │
                                        └─┘
```

---

**Version du protocole**: 1.0
**Compatible avec**: Arduino Uno, Nano, Mega
**Dernière mise à jour**: Décembre 2025

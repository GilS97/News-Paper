# 🚀 Guide d'Installation - Smart Robot Car App

## 📋 Prérequis

### Matériel Requis
- ✅ Ordinateur (Windows, macOS ou Linux)
- ✅ Appareil Android (téléphone ou tablette)
- ✅ Câble USB pour connecter l'appareil
- ✅ Robot Car avec module Bluetooth HC-05/HC-06
- ✅ Code Arduino chargé sur le robot

### Logiciels Requis
- ✅ Android Studio (dernière version)
- ✅ JDK 8 ou supérieur
- ✅ SDK Android (API 24 minimum)

## 🔽 Installation d'Android Studio

### Windows
```
1. Téléchargez depuis: https://developer.android.com/studio
2. Lancez l'installateur
3. Suivez l'assistant d'installation
4. Installez Android SDK 34 et build tools
5. Redémarrez si nécessaire
```

### macOS
```
1. Téléchargez le .dmg
2. Glissez Android Studio dans Applications
3. Lancez Android Studio
4. Suivez le setup wizard
5. Installez les SDK nécessaires
```

### Linux
```bash
# Téléchargez l'archive
wget https://developer.android.com/studio

# Extrayez
tar -xzf android-studio-*.tar.gz

# Lancez
cd android-studio/bin
./studio.sh
```

## 📱 Préparation de l'Appareil Android

### Activer le Mode Développeur

#### Android 12+
```
1. Paramètres → À propos du téléphone
2. Appuyez 7 fois sur "Numéro de build"
3. Retour → Système → Options développeur
4. Activez "Débogage USB"
```

#### Android 11 et antérieur
```
1. Paramètres → À propos du téléphone
2. Appuyez 7 fois sur "Numéro de version"
3. Retour → Options développeur
4. Activez "Débogage USB"
```

### Connecter l'Appareil
```
1. Branchez le câble USB
2. Sur l'appareil: Autorisez le débogage USB
3. Cochez "Toujours autoriser depuis cet ordinateur"
4. Appuyez sur OK
```

## 📂 Obtenir le Projet

### Option 1: Via Git (Recommandé)
```bash
# Cloner le repository
git clone [URL_DU_REPO]/smart-robot-car-app.git

# Entrer dans le dossier
cd smart-robot-car-app
```

### Option 2: Téléchargement Direct
```
1. Téléchargez le ZIP du projet
2. Extrayez dans un dossier de votre choix
3. Notez le chemin du dossier
```

## 🔧 Ouvrir le Projet

### Dans Android Studio

1. **Lancer Android Studio**
   ```
   File → Open
   ```

2. **Sélectionner le Projet**
   ```
   Naviguez vers: smart-robot-car-app/
   Cliquez sur OK
   ```

3. **Synchronisation Gradle**
   ```
   Android Studio démarre la sync automatiquement
   Attendez "Gradle Build Finished" (1-5 minutes)
   ```

4. **Résolution des Problèmes**

   **Si erreur de SDK:**
   ```
   File → Project Structure → SDK Location
   Définissez Android SDK path
   ```

   **Si erreur Gradle:**
   ```
   File → Invalidate Caches / Restart
   Ou: ./gradlew clean build (en ligne de commande)
   ```

## ⚙️ Configuration du Projet

### Vérifier les Paramètres

1. **build.gradle (app)**
   ```gradle
   compileSdk 34
   minSdk 24
   targetSdk 34
   ```

2. **Gradle Wrapper**
   ```
   Gradle 8.2+
   Android Gradle Plugin 8.2.0
   ```

### SDK Manager

```
Tools → SDK Manager

Installer:
✅ Android 14.0 (API 34)
✅ Android 7.0 (API 24)
✅ Android SDK Build-Tools 34.0.0
✅ Android SDK Platform-Tools
✅ Android SDK Command-line Tools
```

## 🏗️ Compiler le Projet

### Via Android Studio

#### Build Debug (Test)
```
Build → Build Bundle(s) / APK(s) → Build APK(s)

Résultat:
app/build/outputs/apk/debug/app-debug.apk
```

#### Build Release (Production)
```
Build → Generate Signed Bundle / APK
→ APK
→ Create new (première fois)
→ Créez un keystore
→ Définissez les mots de passe
→ Release
→ Finish

Résultat:
app/build/outputs/apk/release/app-release.apk
```

### Via Ligne de Commande

#### Sur Windows
```bash
cd smart-robot-car-app
gradlew.bat assembleDebug
```

#### Sur macOS/Linux
```bash
cd smart-robot-car-app
chmod +x gradlew
./gradlew assembleDebug
```

#### APK Généré
```
Emplacement: app/build/outputs/apk/debug/
Fichier: app-debug.apk
Taille: ~5-8 MB
```

## 📲 Installer l'Application

### Méthode 1: Depuis Android Studio (Recommandé)

```
1. Sélectionnez votre appareil dans la liste déroulante
2. Cliquez sur Run ▶️ (Shift+F10)
3. L'app s'installe et se lance automatiquement
```

### Méthode 2: Via ADB

```bash
# Vérifier que l'appareil est connecté
adb devices

# Installer l'APK
adb install app/build/outputs/apk/debug/app-debug.apk

# Lancer l'app
adb shell am start -n com.robotcar.smart/.MainActivity
```

### Méthode 3: Installation Manuelle

```
1. Copiez app-debug.apk sur l'appareil
2. Sur l'appareil:
   - Paramètres → Sécurité
   - Activez "Sources inconnues"
3. Ouvrez le fichier APK
4. Appuyez sur "Installer"
5. Attendez la fin de l'installation
6. Lancez l'app
```

## 🔍 Vérification de l'Installation

### Tests à Effectuer

#### 1. Lancement de l'App
```
✅ L'app se lance sans erreur
✅ Écran d'accueil s'affiche
✅ 6 cartes de mode visibles
✅ Icône Bluetooth présente
```

#### 2. Permissions
```
Au premier lancement, acceptez:
✅ Permission Bluetooth
✅ Permission Localisation (Android < 12)
✅ Permission Bluetooth Connect (Android 12+)
✅ Permission Bluetooth Scan (Android 12+)
```

#### 3. Interface
```
✅ Thème dark bleu s'affiche
✅ Cartes réagissent au toucher (ripple)
✅ Navigation fonctionne
✅ Bouton retour fonctionne
```

## 🔧 Dépannage Compilation

### Erreur: "SDK not found"

**Solution:**
```
File → Project Structure → SDK Location
Définissez: /path/to/Android/Sdk
Ou:
Tools → SDK Manager → Android SDK Location
```

### Erreur: "Gradle sync failed"

**Solution:**
```bash
# Nettoyer le projet
./gradlew clean

# Rebuilder
./gradlew build --refresh-dependencies
```

### Erreur: "Device not found"

**Solution:**
```
1. Vérifiez le câble USB
2. Réactivez le débogage USB
3. Redémarrez adb: adb kill-server && adb start-server
4. Essayez un autre port USB
```

### Erreur: "INSTALL_FAILED_INSUFFICIENT_STORAGE"

**Solution:**
```
1. Libérez de l'espace sur l'appareil (min 50 MB)
2. Supprimez les apps inutilisées
3. Désinstallez l'ancienne version si présente
```

### Erreur: "INSTALL_FAILED_UPDATE_INCOMPATIBLE"

**Solution:**
```
# Désinstaller complètement l'ancienne version
adb uninstall com.robotcar.smart

# Réinstaller
adb install app-debug.apk
```

## 📊 Logs et Debug

### Voir les Logs en Direct

#### Android Studio
```
View → Tool Windows → Logcat
Filtre: com.robotcar.smart
```

#### ADB
```bash
adb logcat | grep "SmartRobotCar\|BluetoothManager"
```

### Activer les Logs Détaillés

Dans `BluetoothManager.java`:
```java
private static final String TAG = "BluetoothManager";
// Les Log.d() sont déjà présents
```

## 🔄 Mise à Jour de l'Application

### Après Modification du Code

```
1. Modifiez le code source
2. Build → Clean Project
3. Build → Rebuild Project
4. Run ▶️
```

### Incrémenter la Version

Dans `app/build.gradle`:
```gradle
defaultConfig {
    versionCode 2      // Incrémenter
    versionName "1.1"  // Mettre à jour
}
```

## 📦 Distribution

### Créer un APK Release

```
1. Build → Generate Signed Bundle / APK
2. Sélectionnez APK
3. Créez/Sélectionnez votre keystore
4. Sélectionnez Release
5. Cochez V1 et V2 Signature
6. Finish
```

### Localisation de l'APK
```
app/build/outputs/apk/release/app-release.apk
```

### Partager l'APK

**Via email:**
```
Attachez le fichier APK
Taille: ~5-8 MB
```

**Via Google Drive:**
```
1. Uploadez l'APK
2. Partagez le lien
3. Destinataires peuvent télécharger et installer
```

**Via Play Store (Optionnel):**
```
1. Créez un compte développeur Google Play ($25 unique)
2. Créez une application
3. Uploadez l'APK/AAB
4. Complétez les informations
5. Soumettez pour review
```

## ✅ Checklist Finale

Avant de considérer l'installation complète:

- [ ] Android Studio installé et configuré
- [ ] Projet ouvert sans erreur
- [ ] Gradle sync réussi
- [ ] Appareil Android connecté
- [ ] Mode développeur activé
- [ ] Débogage USB activé
- [ ] Build réussi (aucune erreur)
- [ ] APK généré
- [ ] App installée sur l'appareil
- [ ] App se lance correctement
- [ ] Permissions accordées
- [ ] Interface s'affiche correctement
- [ ] Navigation fonctionne
- [ ] Prêt pour connexion Bluetooth

## 🎉 Félicitations !

Si tous les points de la checklist sont cochés, l'installation est **complète et réussie** !

Vous pouvez maintenant:
1. Appairer votre robot (voir GUIDE_UTILISATION.md)
2. Tester tous les modes
3. Personnaliser l'application
4. Partager avec d'autres

## 📞 Support

### En cas de problème

1. **Consultez d'abord:**
   - README.md (section Troubleshooting)
   - GUIDE_UTILISATION.md
   - PROTOCOL.md

2. **Vérifiez:**
   - Versions des SDK
   - Connexion USB
   - Espace disque
   - Permissions

3. **Ressources:**
   - Documentation Android: https://developer.android.com
   - Stack Overflow: https://stackoverflow.com
   - GitHub Issues du projet

---

**Guide d'Installation - Version 1.0**
**Dernière mise à jour: Décembre 2025**
**Temps d'installation estimé: 30-60 minutes (première fois)**

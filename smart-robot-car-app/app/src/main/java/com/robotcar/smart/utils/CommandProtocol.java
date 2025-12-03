package com.robotcar.smart.utils;

/**
 * Protocole de communication avec le Robot Car via Bluetooth
 * Basé sur le code Arduino fourni
 */
public class CommandProtocol {

    // Modes de fonctionnement
    public static final String MODE_GYROSCOPE = "%G#";        // Mode pilotage gyroscope
    public static final String MODE_LINE_TRACKING = "%T#";    // Mode suivi de ligne
    public static final String MODE_LIGHT_SEEKING = "%P#";    // Mode recherche de lumière
    public static final String MODE_IR_REMOTE = "%I#";        // Mode télécommande IR
    public static final String MODE_FOLLOW = "%F#";           // Mode suivi ultrasonique
    public static final String MODE_AVOIDANCE = "%A#";        // Mode évitement d'obstacles

    // Commandes de contrôle
    public static final String COMMAND_STOP_MODE = "%Q";      // Arrêter le mode actuel
    public static final String COMMAND_STOP_MOVEMENT = "%S";  // Arrêter le mouvement
    public static final String COMMAND_TURN_LEFT = "%L";      // Tourner à gauche
    public static final String COMMAND_TURN_RIGHT = "%R";     // Tourner à droite

    /**
     * Génère la commande pour changer la vitesse
     *
     * @param speed Vitesse de 0 à 100
     * @param isIncrement true pour incrémenter, false pour décrémenter
     * @return Commande formatée
     */
    public static String setSpeed(int speed, boolean isIncrement) {
        if (speed < 0) speed = 0;
        if (speed > 100) speed = 100;
        char operator = isIncrement ? '+' : '-';
        return String.format("%%%d%c", speed, operator);
    }

    /**
     * Génère la commande pour le mode gyroscope avec angle
     *
     * @param angle Angle de -180 à 180 degrés
     * @return Commande formatée
     */
    public static String setGyroscopeAngle(int angle) {
        if (angle < -180) angle = -180;
        if (angle > 180) angle = 180;
        return String.format("@%d#", angle);
    }

    /**
     * Génère une commande de vitesse directe (utilisée en mode gyroscope)
     *
     * @param speed Vitesse de 0 à 100
     * @return Commande formatée
     */
    public static String setDirectSpeed(int speed) {
        if (speed < 0) speed = 0;
        if (speed > 100) speed = 100;
        return String.format("%%%d+", speed);
    }

    /**
     * Vérifie si une commande est valide
     *
     * @param command Commande à vérifier
     * @return true si valide
     */
    public static boolean isValidCommand(String command) {
        if (command == null || command.isEmpty()) {
            return false;
        }
        return command.startsWith("%") || command.startsWith("@");
    }

    /**
     * Génère une commande personnalisée
     *
     * @param prefix Préfixe de la commande
     * @param value Valeur
     * @param suffix Suffixe
     * @return Commande formatée
     */
    public static String customCommand(String prefix, String value, String suffix) {
        return prefix + value + suffix;
    }
}

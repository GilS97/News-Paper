package com.robotcar.smart.bluetooth;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import androidx.core.app.ActivityCompat;

import java.io.IOException;
import java.io.OutputStream;
import java.util.Set;
import java.util.UUID;

/**
 * Gestionnaire Bluetooth pour la communication avec le Robot Car
 */
public class BluetoothManager {
    private static final String TAG = "BluetoothManager";
    private static final UUID MY_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    private BluetoothAdapter bluetoothAdapter;
    private BluetoothSocket bluetoothSocket;
    private OutputStream outputStream;
    private Context context;
    private Handler mainHandler;

    private boolean isConnected = false;
    private BluetoothConnectionListener connectionListener;

    public interface BluetoothConnectionListener {
        void onConnected();
        void onDisconnected();
        void onError(String error);
    }

    public BluetoothManager(Context context) {
        this.context = context;
        this.bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        this.mainHandler = new Handler(Looper.getMainLooper());
    }

    public void setConnectionListener(BluetoothConnectionListener listener) {
        this.connectionListener = listener;
    }

    /**
     * Vérifie si le Bluetooth est disponible et activé
     */
    public boolean isBluetoothAvailable() {
        if (bluetoothAdapter == null) {
            return false;
        }
        return bluetoothAdapter.isEnabled();
    }

    /**
     * Récupère la liste des appareils Bluetooth appairés
     */
    public Set<BluetoothDevice> getPairedDevices() {
        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.BLUETOOTH_CONNECT)
            != PackageManager.PERMISSION_GRANTED) {
            return null;
        }
        if (bluetoothAdapter != null) {
            return bluetoothAdapter.getBondedDevices();
        }
        return null;
    }

    /**
     * Connecte à un appareil Bluetooth
     */
    public void connect(final BluetoothDevice device) {
        new Thread(() -> {
            try {
                if (ActivityCompat.checkSelfPermission(context, Manifest.permission.BLUETOOTH_CONNECT)
                    != PackageManager.PERMISSION_GRANTED) {
                    notifyError("Bluetooth permission not granted");
                    return;
                }

                // Fermer la connexion existante si elle existe
                disconnect();

                Log.d(TAG, "Connecting to device: " + device.getName());
                bluetoothSocket = device.createRfcommSocketToServiceRecord(MY_UUID);
                bluetoothSocket.connect();
                outputStream = bluetoothSocket.getOutputStream();

                isConnected = true;
                notifyConnected();
                Log.d(TAG, "Connected successfully");

            } catch (IOException e) {
                Log.e(TAG, "Connection failed", e);
                isConnected = false;
                notifyError("Connection failed: " + e.getMessage());
                closeConnection();
            }
        }).start();
    }

    /**
     * Déconnecte l'appareil Bluetooth
     */
    public void disconnect() {
        isConnected = false;
        closeConnection();
        notifyDisconnected();
    }

    /**
     * Ferme la connexion Bluetooth
     */
    private void closeConnection() {
        try {
            if (outputStream != null) {
                outputStream.close();
                outputStream = null;
            }
            if (bluetoothSocket != null) {
                bluetoothSocket.close();
                bluetoothSocket = null;
            }
        } catch (IOException e) {
            Log.e(TAG, "Error closing connection", e);
        }
    }

    /**
     * Envoie une commande au robot
     */
    public boolean sendCommand(String command) {
        if (!isConnected || outputStream == null) {
            Log.w(TAG, "Not connected, cannot send command");
            return false;
        }

        try {
            outputStream.write(command.getBytes());
            outputStream.flush();
            Log.d(TAG, "Command sent: " + command);
            return true;
        } catch (IOException e) {
            Log.e(TAG, "Error sending command", e);
            isConnected = false;
            notifyError("Error sending command: " + e.getMessage());
            return false;
        }
    }

    /**
     * Vérifie si le Bluetooth est connecté
     */
    public boolean isConnected() {
        return isConnected && bluetoothSocket != null && bluetoothSocket.isConnected();
    }

    // Méthodes de notification
    private void notifyConnected() {
        if (connectionListener != null) {
            mainHandler.post(() -> connectionListener.onConnected());
        }
    }

    private void notifyDisconnected() {
        if (connectionListener != null) {
            mainHandler.post(() -> connectionListener.onDisconnected());
        }
    }

    private void notifyError(String error) {
        if (connectionListener != null) {
            mainHandler.post(() -> connectionListener.onError(error));
        }
    }

    /**
     * Libère les ressources
     */
    public void release() {
        disconnect();
        connectionListener = null;
    }
}

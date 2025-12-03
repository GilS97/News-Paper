package com.robotcar.smart.bluetooth;

import android.app.Application;
import android.bluetooth.BluetoothDevice;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.robotcar.smart.utils.CommandProtocol;

import java.util.Set;

/**
 * ViewModel pour gérer l'état Bluetooth dans toute l'application
 */
public class BluetoothViewModel extends AndroidViewModel {

    private BluetoothManager bluetoothManager;
    private MutableLiveData<Boolean> isConnected = new MutableLiveData<>(false);
    private MutableLiveData<String> connectionStatus = new MutableLiveData<>("Not connected");
    private MutableLiveData<String> errorMessage = new MutableLiveData<>();
    private MutableLiveData<Integer> currentSpeed = new MutableLiveData<>(60);

    public BluetoothViewModel(@NonNull Application application) {
        super(application);
        bluetoothManager = new BluetoothManager(application.getApplicationContext());
        setupBluetoothListener();
    }

    private void setupBluetoothListener() {
        bluetoothManager.setConnectionListener(new BluetoothManager.BluetoothConnectionListener() {
            @Override
            public void onConnected() {
                isConnected.postValue(true);
                connectionStatus.postValue("Connected");
            }

            @Override
            public void onDisconnected() {
                isConnected.postValue(false);
                connectionStatus.postValue("Disconnected");
            }

            @Override
            public void onError(String error) {
                isConnected.postValue(false);
                connectionStatus.postValue("Error");
                errorMessage.postValue(error);
            }
        });
    }

    // LiveData getters
    public LiveData<Boolean> getIsConnected() {
        return isConnected;
    }

    public LiveData<String> getConnectionStatus() {
        return connectionStatus;
    }

    public LiveData<String> getErrorMessage() {
        return errorMessage;
    }

    public LiveData<Integer> getCurrentSpeed() {
        return currentSpeed;
    }

    // Bluetooth operations
    public boolean isBluetoothAvailable() {
        return bluetoothManager.isBluetoothAvailable();
    }

    public Set<BluetoothDevice> getPairedDevices() {
        return bluetoothManager.getPairedDevices();
    }

    public void connect(BluetoothDevice device) {
        bluetoothManager.connect(device);
    }

    public void disconnect() {
        bluetoothManager.disconnect();
    }

    // Command sending methods
    public boolean sendCommand(String command) {
        return bluetoothManager.sendCommand(command);
    }

    public void startMode(String modeCommand) {
        sendCommand(modeCommand);
    }

    public void stopCurrentMode() {
        sendCommand(CommandProtocol.COMMAND_STOP_MODE);
    }

    public void stopMovement() {
        sendCommand(CommandProtocol.COMMAND_STOP_MOVEMENT);
    }

    public void turnLeft() {
        sendCommand(CommandProtocol.COMMAND_TURN_LEFT);
    }

    public void turnRight() {
        sendCommand(CommandProtocol.COMMAND_TURN_RIGHT);
    }

    public void setSpeed(int speed) {
        if (speed >= 0 && speed <= 100) {
            currentSpeed.postValue(speed);
            sendCommand(CommandProtocol.setDirectSpeed(speed));
        }
    }

    public void sendGyroscopeAngle(int angle) {
        sendCommand(CommandProtocol.setGyroscopeAngle(angle));
    }

    @Override
    protected void onCleared() {
        super.onCleared();
        bluetoothManager.release();
    }
}

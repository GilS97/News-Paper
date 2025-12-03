package com.robotcar.smart.ui.remotecontrol;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android:os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.widget.SwitchCompat;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;

import com.google.android.material.button.MaterialButton;
import com.robotcar.smart.R;
import com.robotcar.smart.bluetooth.BluetoothViewModel;
import com.robotcar.smart.utils.CommandProtocol;
import com.robotcar.smart.views.JoystickView;

public class RemoteControlFragment extends Fragment implements SensorEventListener {

    private BluetoothViewModel bluetoothViewModel;
    private SensorManager sensorManager;
    private Sensor accelerometer;

    private JoystickView joystickView;
    private SwitchCompat gravitySensorSwitch;
    private TextView speedValueText;
    private TextView connectionStatusText;
    private ProgressBar speedProgressBar;
    private ImageView bluetoothIcon;

    private int currentSpeed = 60;
    private boolean isGravitySensorMode = false;
    private boolean isJoystickActive = false;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_remote_control, container, false);

        // Initialize ViewModel
        bluetoothViewModel = new ViewModelProvider(requireActivity()).get(BluetoothViewModel.class);

        // Initialize sensor manager
        sensorManager = (SensorManager) requireActivity().getSystemService(Context.SENSOR_SERVICE);
        if (sensorManager != null) {
            accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        }

        // Initialize views
        initializeViews(view);

        // Setup listeners
        setupListeners();

        // Observe connection status
        observeConnectionStatus();

        // Activate gyroscope mode
        bluetoothViewModel.startMode(CommandProtocol.MODE_GYROSCOPE);

        return view;
    }

    private void initializeViews(View view) {
        ImageButton backButton = view.findViewById(R.id.backButton);
        backButton.setOnClickListener(v -> {
            bluetoothViewModel.stopCurrentMode();
            Navigation.findNavController(v).navigateUp();
        });

        joystickView = view.findViewById(R.id.joystickView);
        gravitySensorSwitch = view.findViewById(R.id.gravitySensorSwitch);
        speedValueText = view.findViewById(R.id.speedValueText);
        connectionStatusText = view.findViewById(R.id.connectionStatusText);
        speedProgressBar = view.findViewById(R.id.speedProgressBar);
        bluetoothIcon = view.findViewById(R.id.bluetoothIcon);

        MaterialButton decreaseSpeedButton = view.findViewById(R.id.decreaseSpeedButton);
        MaterialButton increaseSpeedButton = view.findViewById(R.id.increaseSpeedButton);
        MaterialButton rotateLeftButton = view.findViewById(R.id.rotateLeftButton);
        MaterialButton rotateRightButton = view.findViewById(R.id.rotateRightButton);

        decreaseSpeedButton.setOnClickListener(v -> adjustSpeed(-10));
        increaseSpeedButton.setOnClickListener(v -> adjustSpeed(10));
        rotateLeftButton.setOnClickListener(v -> bluetoothViewModel.turnLeft());
        rotateRightButton.setOnClickListener(v -> bluetoothViewModel.turnRight());
    }

    private void setupListeners() {
        // Joystick listener
        joystickView.setJoystickListener(new JoystickView.JoystickListener() {
            @Override
            public void onJoystickMoved(int angle, int strength) {
                if (!isGravitySensorMode && strength > 10) {
                    isJoystickActive = true;
                    bluetoothViewModel.sendGyroscopeAngle(angle);
                }
            }

            @Override
            public void onJoystickReleased() {
                if (!isGravitySensorMode) {
                    isJoystickActive = false;
                    bluetoothViewModel.stopMovement();
                }
            }
        });

        // Gravity sensor switch
        gravitySensorSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> {
            isGravitySensorMode = isChecked;
            if (isChecked) {
                startGravitySensor();
                joystickView.setEnabled(false);
                joystickView.setAlpha(0.5f);
            } else {
                stopGravitySensor();
                joystickView.setEnabled(true);
                joystickView.setAlpha(1.0f);
                if (!isJoystickActive) {
                    bluetoothViewModel.stopMovement();
                }
            }
        });
    }

    private void adjustSpeed(int delta) {
        currentSpeed += delta;
        if (currentSpeed < 0) currentSpeed = 0;
        if (currentSpeed > 100) currentSpeed = 100;

        updateSpeedDisplay();
        bluetoothViewModel.setSpeed(currentSpeed);
    }

    private void updateSpeedDisplay() {
        speedValueText.setText(String.valueOf(currentSpeed));
        speedProgressBar.setProgress(currentSpeed);
    }

    private void startGravitySensor() {
        if (sensorManager != null && accelerometer != null) {
            sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_GAME);
        }
    }

    private void stopGravitySensor() {
        if (sensorManager != null) {
            sensorManager.unregisterListener(this);
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER && isGravitySensorMode) {
            float x = event.values[0];
            float y = event.values[1];

            // Calculate angle from gravity sensor
            // x: -10 to 10, y: -10 to 10
            // Convert to angle -180 to 180
            float angle = (float) Math.toDegrees(Math.atan2(x, y));

            // Only send if significant tilt
            if (Math.abs(x) > 1.5 || Math.abs(y) > 1.5) {
                bluetoothViewModel.sendGyroscopeAngle((int) angle);
            } else {
                bluetoothViewModel.stopMovement();
            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // Not used
    }

    private void observeConnectionStatus() {
        bluetoothViewModel.getIsConnected().observe(getViewLifecycleOwner(), isConnected -> {
            if (isConnected) {
                bluetoothIcon.setColorFilter(getResources().getColor(R.color.bluetooth_connected));
                connectionStatusText.setText(R.string.bluetooth_connected);
                connectionStatusText.setTextColor(getResources().getColor(R.color.bluetooth_connected));
            } else {
                bluetoothIcon.setColorFilter(getResources().getColor(R.color.bluetooth_disconnected));
                connectionStatusText.setText(R.string.bluetooth_not_connected);
                connectionStatusText.setTextColor(getResources().getColor(R.color.text_secondary));
            }
        });

        bluetoothViewModel.getCurrentSpeed().observe(getViewLifecycleOwner(), speed -> {
            currentSpeed = speed;
            updateSpeedDisplay();
        });
    }

    @Override
    public void onPause() {
        super.onPause();
        stopGravitySensor();
        bluetoothViewModel.stopMovement();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        stopGravitySensor();
        bluetoothViewModel.stopCurrentMode();
    }
}

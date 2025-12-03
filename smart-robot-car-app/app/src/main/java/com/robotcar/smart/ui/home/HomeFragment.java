package com.robotcar.smart.ui.home;

import android.app.AlertDialog;
import android.bluetooth.BluetoothDevice;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;

import com.google.android.material.card.MaterialCardView;
import com.robotcar.smart.R;
import com.robotcar.smart.bluetooth.BluetoothViewModel;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class HomeFragment extends Fragment {

    private BluetoothViewModel bluetoothViewModel;
    private ImageView bluetoothIcon;
    private TextView connectionStatusText;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_home, container, false);

        // Initialize ViewModel
        bluetoothViewModel = new ViewModelProvider(requireActivity()).get(BluetoothViewModel.class);

        // Initialize views
        bluetoothIcon = view.findViewById(R.id.bluetoothIcon);
        connectionStatusText = view.findViewById(R.id.connectionStatusText);

        // Setup card clicks
        setupModeCards(view);

        // Setup Bluetooth icon click
        bluetoothIcon.setOnClickListener(v -> handleBluetoothIconClick());

        // Observe connection status
        observeConnectionStatus();

        return view;
    }

    private void setupModeCards(View view) {
        MaterialCardView cardRemoteControl = view.findViewById(R.id.cardRemoteControl);
        MaterialCardView cardLineTracking = view.findViewById(R.id.cardLineTracking);
        MaterialCardView cardAvoidObstacles = view.findViewById(R.id.cardAvoidObstacles);
        MaterialCardView cardUltrasound = view.findViewById(R.id.cardUltrasound);
        MaterialCardView cardIrRemote = view.findViewById(R.id.cardIrRemote);
        MaterialCardView cardLightSeeking = view.findViewById(R.id.cardLightSeeking);

        cardRemoteControl.setOnClickListener(v -> {
            if (checkBluetoothConnection()) {
                Navigation.findNavController(v).navigate(R.id.action_home_to_remoteControl);
            }
        });

        cardLineTracking.setOnClickListener(v -> {
            if (checkBluetoothConnection()) {
                Navigation.findNavController(v).navigate(R.id.action_home_to_lineTracking);
            }
        });

        cardAvoidObstacles.setOnClickListener(v -> {
            if (checkBluetoothConnection()) {
                Navigation.findNavController(v).navigate(R.id.action_home_to_avoidObstacles);
            }
        });

        cardUltrasound.setOnClickListener(v -> {
            if (checkBluetoothConnection()) {
                Navigation.findNavController(v).navigate(R.id.action_home_to_followMe);
            }
        });

        cardIrRemote.setOnClickListener(v -> {
            if (checkBluetoothConnection()) {
                Navigation.findNavController(v).navigate(R.id.action_home_to_irRemote);
            }
        });

        cardLightSeeking.setOnClickListener(v -> {
            if (checkBluetoothConnection()) {
                Navigation.findNavController(v).navigate(R.id.action_home_to_lightSeeking);
            }
        });
    }

    private void handleBluetoothIconClick() {
        Boolean isConnected = bluetoothViewModel.getIsConnected().getValue();
        if (isConnected != null && isConnected) {
            // Show disconnect dialog
            showDisconnectDialog();
        } else {
            // Show connect dialog
            showConnectDialog();
        }
    }

    private void showConnectDialog() {
        if (!bluetoothViewModel.isBluetoothAvailable()) {
            Toast.makeText(requireContext(),
                    "Bluetooth is not available or not enabled",
                    Toast.LENGTH_SHORT).show();
            return;
        }

        Set<BluetoothDevice> pairedDevices = bluetoothViewModel.getPairedDevices();
        if (pairedDevices == null || pairedDevices.isEmpty()) {
            Toast.makeText(requireContext(),
                    "No paired Bluetooth devices found",
                    Toast.LENGTH_SHORT).show();
            return;
        }

        List<BluetoothDevice> deviceList = new ArrayList<>(pairedDevices);
        List<String> deviceNames = new ArrayList<>();
        for (BluetoothDevice device : deviceList) {
            String deviceName = device.getName();
            deviceNames.add(deviceName != null ? deviceName : device.getAddress());
        }

        ArrayAdapter<String> adapter = new ArrayAdapter<>(requireContext(),
                android.R.layout.select_dialog_item, deviceNames);

        new AlertDialog.Builder(requireContext())
                .setTitle("Connect to Robot")
                .setAdapter(adapter, (dialog, which) -> {
                    BluetoothDevice selectedDevice = deviceList.get(which);
                    bluetoothViewModel.connect(selectedDevice);
                    Toast.makeText(requireContext(),
                            "Connecting to " + deviceNames.get(which),
                            Toast.LENGTH_SHORT).show();
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void showDisconnectDialog() {
        new AlertDialog.Builder(requireContext())
                .setTitle("Disconnect")
                .setMessage("Do you want to disconnect from the robot?")
                .setPositiveButton("Disconnect", (dialog, which) -> {
                    bluetoothViewModel.disconnect();
                    Toast.makeText(requireContext(), "Disconnected", Toast.LENGTH_SHORT).show();
                })
                .setNegativeButton("Cancel", null)
                .show();
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

        bluetoothViewModel.getErrorMessage().observe(getViewLifecycleOwner(), error -> {
            if (error != null && !error.isEmpty()) {
                Toast.makeText(requireContext(), error, Toast.LENGTH_SHORT).show();
            }
        });
    }

    private boolean checkBluetoothConnection() {
        Boolean isConnected = bluetoothViewModel.getIsConnected().getValue();
        if (isConnected == null || !isConnected) {
            Toast.makeText(requireContext(),
                    "Please connect to the robot first",
                    Toast.LENGTH_SHORT).show();
            return false;
        }
        return true;
    }
}

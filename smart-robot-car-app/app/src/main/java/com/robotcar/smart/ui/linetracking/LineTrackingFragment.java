package com.robotcar.smart.ui.linetracking;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;

import com.google.android.material.button.MaterialButton;
import com.robotcar.smart.R;
import com.robotcar.smart.bluetooth.BluetoothViewModel;
import com.robotcar.smart.utils.CommandProtocol;

public class LineTrackingFragment extends Fragment {

    private BluetoothViewModel bluetoothViewModel;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_autonomous_mode, container, false);

        bluetoothViewModel = new ViewModelProvider(requireActivity()).get(BluetoothViewModel.class);

        setupViews(view);
        observeConnectionStatus(view);

        // Start line tracking mode
        bluetoothViewModel.startMode(CommandProtocol.MODE_LINE_TRACKING);

        return view;
    }

    private void setupViews(View view) {
        TextView titleText = view.findViewById(R.id.titleText);
        titleText.setText(R.string.line_tracking);

        ImageView modeIcon = view.findViewById(R.id.modeIcon);
        modeIcon.setImageResource(android.R.drawable.ic_menu_directions);

        TextView descriptionText = view.findViewById(R.id.descriptionText);
        descriptionText.setText("The robot is following the line on the track");

        ImageButton backButton = view.findViewById(R.id.backButton);
        backButton.setOnClickListener(v -> {
            bluetoothViewModel.stopCurrentMode();
            Navigation.findNavController(v).navigateUp();
        });

        MaterialButton stopButton = view.findViewById(R.id.stopButton);
        stopButton.setOnClickListener(v -> {
            bluetoothViewModel.stopCurrentMode();
            Navigation.findNavController(v).navigateUp();
        });
    }

    private void observeConnectionStatus(View view) {
        ImageView bluetoothIcon = view.findViewById(R.id.bluetoothIcon);
        bluetoothViewModel.getIsConnected().observe(getViewLifecycleOwner(), isConnected -> {
            if (isConnected) {
                bluetoothIcon.setColorFilter(getResources().getColor(R.color.bluetooth_connected));
            } else {
                bluetoothIcon.setColorFilter(getResources().getColor(R.color.bluetooth_disconnected));
            }
        });
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        bluetoothViewModel.stopCurrentMode();
    }
}

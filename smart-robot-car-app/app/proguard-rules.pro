# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# Keep Bluetooth classes
-keep class android.bluetooth.** { *; }
-keep interface android.bluetooth.** { *; }

# Keep custom views
-keep public class com.robotcar.smart.views.** { *; }

# Keep navigation components
-keepnames class androidx.navigation.fragment.NavHostFragment

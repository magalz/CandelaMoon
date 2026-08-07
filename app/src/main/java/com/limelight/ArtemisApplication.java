package com.limelight;

import android.app.Application;
import android.widget.Toast;

import com.limelight.profiles.ProfilesManager;

public class ArtemisApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        ProfilesManager profilesManager = ProfilesManager.getInstance();
        if (!profilesManager.load(this)) {
            // A directly-constructed Application (unit tests) has no attached base Context;
            // Toast.makeText would NPE on it. Profile loading above always runs, so the
            // real attached startup contract is preserved.
            if (getBaseContext() != null) {
                Toast.makeText(this, R.string.profile_manager_failed_to_load, Toast.LENGTH_LONG).show();
            }
        }
    }
}

package com.limelight;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;

import androidx.test.core.app.ApplicationProvider;

import com.google.android.material.floatingactionbutton.ExtendedFloatingActionButton;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.annotation.Config;

import static org.junit.Assert.*;

@Config(sdk = {28, 29, 30, 33})
@RunWith(RobolectricTestRunner.class)
public class MaterialFabCompatTest {
    @BeforeClass
    public static void suppressInvalidIdLogs() {
        TestLogSuppressor.install();
    }

    private static Context appCompatContext() {
        Context base = ApplicationProvider.getApplicationContext();
        return new androidx.appcompat.view.ContextThemeWrapper(base,
                androidx.appcompat.R.style.Theme_AppCompat);
    }

    private static Context productionContext() {
        Context base = ApplicationProvider.getApplicationContext();
        return new androidx.appcompat.view.ContextThemeWrapper(base, R.style.AppTheme);
    }

    @Test
    public void fabLayoutsInflateUnderProductionThemeAcrossApiTiers() {
        // Production themes: Theme.MaterialComponents on API <= 28 (values/v21) and
        // Theme.Material3.Dark.NoActionBar on API >= 29 (values-v29). Both variants must
        // keep the Material FABs rendering as Material widgets at every supported tier.
        Context context = productionContext();
        assertFabInflates(context, R.layout.activity_app_view, R.id.profilesButton, ExtendedFloatingActionButton.class);
        assertFabInflates(context, R.layout.activity_pc_view, R.id.profilesButton, ExtendedFloatingActionButton.class);
        assertFabInflates(context, R.layout.activity_profiles, R.id.addProfileFab, FloatingActionButton.class);
    }

    @Test
    public void fabLayoutsInflateUnderAppCompatThemeAcrossApiTiers() {
        // The P1-021 inflation contract under Theme_AppCompat (non-Material), which is the
        // production context for ProfilesActivity's FAB on API <= 28 (SettingsTheme is an
        // AppCompat theme below API 29).
        Context context = appCompatContext();
        assertFabInflates(context, R.layout.activity_app_view, R.id.profilesButton, ExtendedFloatingActionButton.class);
        assertFabInflates(context, R.layout.activity_pc_view, R.id.profilesButton, ExtendedFloatingActionButton.class);
        assertFabInflates(context, R.layout.activity_profiles, R.id.addProfileFab, FloatingActionButton.class);
    }

    @Test
    @Config(qualifiers = "land")
    public void landscapePcViewFabInflatesAcrossApiTiers() {
        // layout-land/activity_pc_view.xml is the alternate-resource variant of the
        // PcView layout; the FAB workaround must hold there under both theme families.
        assertFabInflates(productionContext(), R.layout.activity_pc_view, R.id.profilesButton, ExtendedFloatingActionButton.class);
        assertFabInflates(appCompatContext(), R.layout.activity_pc_view, R.id.profilesButton, ExtendedFloatingActionButton.class);
    }

    @Test
    public void materialEnforcementStillActiveForUnscopedWidgets() {
        // The workaround styles relax enforcement only on the four scoped FAB instances;
        // an unscoped Material widget must still fail under Theme_AppCompat and must pass
        // under the production theme at every supported API tier (Material2 / Material3).
        try {
            new ExtendedFloatingActionButton(appCompatContext());
            fail("Unscoped Material widget must still enforce the Material theme under Theme_AppCompat");
        } catch (IllegalArgumentException expected) {
            // Enforcement is active outside the scoped workaround styles.
        }
        new ExtendedFloatingActionButton(productionContext());
    }

    private static void assertFabInflates(Context context, int layoutId, int fabId, Class<?> expectedType) {
        try {
            View root = LayoutInflater.from(context).inflate(layoutId, null);
            View fab = root.findViewById(fabId);
            assertNotNull("FAB not found in layout " + layoutId, fab);
            assertTrue("FAB in layout " + layoutId + " should be " + expectedType.getSimpleName()
                    + " but was " + fab.getClass().getName(), expectedType.isInstance(fab));
        } catch (android.view.InflateException e) {
            fail("Layout " + layoutId + " must inflate without InflateException: " + e.getMessage());
        }
    }
}

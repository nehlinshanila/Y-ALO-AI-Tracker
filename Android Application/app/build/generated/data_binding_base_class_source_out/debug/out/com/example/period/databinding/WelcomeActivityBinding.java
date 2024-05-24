// Generated by view binder compiler. Do not edit!
package com.example.period.databinding;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CalendarView;
import android.widget.LinearLayout;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.viewbinding.ViewBinding;
import androidx.viewbinding.ViewBindings;
import com.example.period.R;
import java.lang.NullPointerException;
import java.lang.Override;
import java.lang.String;

public final class WelcomeActivityBinding implements ViewBinding {
  @NonNull
  private final LinearLayout rootView;

  @NonNull
  public final CalendarView calendarView;

  @NonNull
  public final Button logPeriodButton;

  @NonNull
  public final Button moreOptionsButton;

  private WelcomeActivityBinding(@NonNull LinearLayout rootView, @NonNull CalendarView calendarView,
      @NonNull Button logPeriodButton, @NonNull Button moreOptionsButton) {
    this.rootView = rootView;
    this.calendarView = calendarView;
    this.logPeriodButton = logPeriodButton;
    this.moreOptionsButton = moreOptionsButton;
  }

  @Override
  @NonNull
  public LinearLayout getRoot() {
    return rootView;
  }

  @NonNull
  public static WelcomeActivityBinding inflate(@NonNull LayoutInflater inflater) {
    return inflate(inflater, null, false);
  }

  @NonNull
  public static WelcomeActivityBinding inflate(@NonNull LayoutInflater inflater,
      @Nullable ViewGroup parent, boolean attachToParent) {
    View root = inflater.inflate(R.layout.welcome_activity, parent, false);
    if (attachToParent) {
      parent.addView(root);
    }
    return bind(root);
  }

  @NonNull
  public static WelcomeActivityBinding bind(@NonNull View rootView) {
    // The body of this method is generated in a way you would not otherwise write.
    // This is done to optimize the compiled bytecode for size and performance.
    int id;
    missingId: {
      id = R.id.calendarView;
      CalendarView calendarView = ViewBindings.findChildViewById(rootView, id);
      if (calendarView == null) {
        break missingId;
      }

      id = R.id.logPeriodButton;
      Button logPeriodButton = ViewBindings.findChildViewById(rootView, id);
      if (logPeriodButton == null) {
        break missingId;
      }

      id = R.id.moreOptionsButton;
      Button moreOptionsButton = ViewBindings.findChildViewById(rootView, id);
      if (moreOptionsButton == null) {
        break missingId;
      }

      return new WelcomeActivityBinding((LinearLayout) rootView, calendarView, logPeriodButton,
          moreOptionsButton);
    }
    String missingId = rootView.getResources().getResourceName(id);
    throw new NullPointerException("Missing required view with ID: ".concat(missingId));
  }
}
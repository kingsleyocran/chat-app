export function notifyUser(message, user) {
  if (checkNotificationStatus()) {
    const notification = new Notification(message, {
      body: `From: ${user}`,
    });
    notification.onclick = () => {
      window.focus();
      notification.close();
    };
  } else {
    alert("You do not have permission to notify");
  }
}

export function checkNotificationStatus() {
  if (!(Notification in window)) {
    alert("Your browser does not support notifications");
  } else {
    switch (Notification.permission) {
      case "granted":
        return true;
      case "denied":
        return false;
      default:
        Notification.requestPermission(function (status) {
          return status === "granted";
        });
    }
  }
}

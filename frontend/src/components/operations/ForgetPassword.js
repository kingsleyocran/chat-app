import React from "react";

export default function ForgetPassword() {
  return (
    <div>
      <div>
        <form>
          <input type="password" placeholder="Enter your password" />
          <input type="password" placeholder="Re-Type your password" />
          <button>Submit</button>
        </form>
      </div>
    </div>
  );
}

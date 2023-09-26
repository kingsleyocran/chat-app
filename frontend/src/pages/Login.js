import React, { useState } from "react";
import LoginForm from "../components/form/LoginForm";
import { logUserIn } from "../utils/operations";
import { useNavigate } from "react-router-dom";
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";

export default function Login() {
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");
  const [open, setOpen] = React.useState(false);

  const handleSubmit = async (e, user) => {
    setOpen(true);
    e.preventDefault();

    try {
      await logUserIn(user);
      navigate("/");
    } catch (e) {
      setErrorMessage(e.error);
    } finally {
      setOpen(false);
    }
  };

  return (
    <div>
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={open}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
      <LoginForm
        handleSubmit={handleSubmit}
        errorMessage={errorMessage}
        setErrorMessage={setErrorMessage}
      />
    </div>
  );
}

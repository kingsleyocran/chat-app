import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../../utils/operations";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import InputAdornment from "@mui/material/InputAdornment";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import FormControl from "@mui/material/FormControl";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";
import Collapse from "@mui/material/Collapse";
import CloseIcon from "@mui/icons-material/Close";

import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";

export default function RegisterForm() {
  const navigate = useNavigate();

  const [user, setUser] = useState({
    username: "",
    password: "",
    passwordRetake: "",
    email: "",
  });

  const [errorMessage, setErrorMessage] = useState("");
  const [open, setOpen] = React.useState(false);
  const [showPassword, setShowPassword] = React.useState(false);
  const [showPassword1, setShowPassword1] = React.useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);
  const handleClickShowPassword1 = () => setShowPassword1((show) => !show);
  const handleUsernameChange = (event) => {
    setUser((prevUserState) => ({
      ...prevUserState,
      username: event.target.value,
    }));
  };

  const handleEmailChange = (event) => {
    setUser((prevUserState) => ({
      ...prevUserState,
      email: event.target.value,
    }));
  };

  const handlePasswordChange = (event) => {
    setUser((prevUserState) => ({
      ...prevUserState,
      password: event.target.value,
    }));
  };

  const handlePasswordRetakeChange = (event) => {
    setUser((prevUserState) => ({
      ...prevUserState,
      passwordRetake: event.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (user.password !== user.passwordRetake) {
        setOpen(true);
        setErrorMessage("Mismatch password");
      } else {
        const success = await registerUser(user);
        if (success) {
          navigate("/login", {
            state: { message: "Verify email and try to Log In" },
          });
        }
      }
    } catch (e) {
      setErrorMessage(e.error || e.detail);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          Sign Up
        </Typography>
        <Collapse in={open}>
          <Alert
            severity="error"
            action={
              <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                  setOpen(false);
                }}
              >
                <CloseIcon fontSize="inherit" />
              </IconButton>
            }
            sx={{ mb: 2 }}
          >
            {errorMessage}
          </Alert>
        </Collapse>
        <Box
          component="form"
          onSubmit={handleSubmit}
          validate="true"
          sx={{ mt: 1 }}
        >
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="text"
            autoComplete="email"
            autoFocus
            value={user.username}
            onChange={handleUsernameChange}
          />

          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email"
            name="email"
            autoComplete="email"
            value={user.email}
            onChange={handleEmailChange}
          />

          <FormControl fullWidth variant="outlined" sx={{ mt: 3, mb: 2 }}>
            <InputLabel>Password</InputLabel>
            <OutlinedInput
              required
              name="password"
              id="password"
              type={showPassword ? "text" : "password"}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={handleClickShowPassword}
                    edge="end"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              }
              label="Password"
              onChange={handlePasswordChange}
              value={user.password}
              autoComplete="current-password"
            />
          </FormControl>

          <FormControl fullWidth variant="outlined" sx={{ mt: 3, mb: 2 }}>
            <InputLabel>Re-Type Password</InputLabel>
            <OutlinedInput
              required
              name="password"
              id="password-retype"
              type={showPassword1 ? "text" : "password"}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={handleClickShowPassword1}
                    edge="end"
                  >
                    {showPassword1 ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              }
              label="Re-Type Password"
              onChange={handlePasswordRetakeChange}
              value={user.passwordRetake}
              autoComplete="current-password"
            />
          </FormControl>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Submit
          </Button>
          <Grid container>
            <Grid item xs>
              <Link
                to="/login"
                variant="body2"
                style={{ textDecoration: "none" }}
              >
                Already have an Account? Login
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}

import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

export default function Layout() {
  const [value, setValue] = useState(true);

  const Theme = createTheme({
    palette: {
      mode: value ? "light" : "dark",
    },
    components: {
      MuiListItemButton: {
        styleOverrides: {
          root: {
            "&.Mui-selected": {
              backgroundColor: value ? "#2196f3" : "#5393ff",
            },
          },
        },
      },
    },
  });

  return (
    <ThemeProvider theme={Theme}>
      <CssBaseline />
      <div>
        <Outlet context={{ setValue: setValue, value: value }} />
      </div>
    </ThemeProvider>
  );
}

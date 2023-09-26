import React, { useEffect, useState, useRef } from "react";
import ChatArea from "../components/chat/ChatArea";
import ChatUsers from "../components/chat/ChatUsers";
import { useNavigate, useOutletContext } from "react-router-dom";
import {
  logOut,
  getUsername,
  SearchUser,
  getAllUsers,
} from "../utils/operations";

import Logout from "@mui/icons-material/Logout";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import Divider from "@mui/material/Divider";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Tooltip from "@mui/material/Tooltip";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Switch from "@mui/material/Switch";
import FormControlLabel from "@mui/material/FormControlLabel";
import { useStyles } from "../styles/chat";
import { createWebSocket } from "../utils/websocket";

export default function Chat() {
  /** Define all states in the Chat Page */
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [chatWith, setChatWith] = useState("");
  const users = useRef([]);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const classes = useStyles();
  const { setValue, value } = useOutletContext();
  const websocket = useRef(null);

  // test sample of users
  // {
  //   USERNAME: "david",
  //   STAR: true,
  //   // PROFILE_PIC: "https://material-ui.com/static/images/avatar/2.jpg",
  //   IS_ACTIVE: true,
  // },
  // {
  //   USERNAME: "ama",
  //   STAR: false,
  //   // PROFILE_PIC: "https://material-ui.com/static/images/avatar/3.jpg",
  //   IS_ACTIVE: false,
  // },
  // {
  //   USERNAME: "Remy Sharp",
  //   STAR: true,
  //   // PROFILE_PIC: "https://material-ui.com/static/images/avatar/4.jpg",
  //   IS_ACTIVE: true,
  // },
  // {
  //   USERNAME: "Alice",
  //   STAR: false,
  //   // PROFILE_PIC: "https://material-ui.com/static/images/avatar/5.jpg",
  //   IS_ACTIVE: false,
  // },
  // {
  //   USERNAME: "Cindy Baker",
  //   STAR: true,
  //   // PROFILE_PIC: "https://material-ui.com/static/images/avatar/6.jpg",
  //   IS_ACTIVE: true,
  // },

  // Call startup functions
  useEffect(() => {
    websocket.current = createWebSocket("ghana");
    websocket.current.onopen = () => {
      console.log("connected");
    };
    const currentWebSocket = websocket.current;

    async function fetchData() {
      const response_users = await getAllUsers();
      if (response_users !== null) {
        users.current = response_users;
        console.log("Response", response_users);
      }

      const response = await getUsername();
      if (response !== null) {
        setUsername(response);
      } else if (response === undefined) {
        window.location.reload();
      } else {
        navigate("/login");
      }
    }
    fetchData();

    return () => {
      currentWebSocket.close();
    };
  }, [users, navigate, websocket]);

  /** Define all handlers for operations here */
  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const toggleTheme = () => {
    setValue((prev) => !prev);
  };

  const handleFocus = () => {
    // reestablish the connection when it's down
    if (websocket.current?.readyState === WebSocket.CLOSED) {
      websocket.current.onopen = () => {
        console.log("connected");
      };
    }
  };

  const handleLogOut = async (e) => {
    e.preventDefault();
    await logOut();
    handleClose();
    setValue(true);
    navigate("/login");
  };
  if (username) {
    return (
      <>
        <Grid container>
          <Grid container height={44} alignContent="center">
            <Typography
              variant="h5"
              letterSpacing={1.5}
              className="header-message"
              paddingLeft={6}
              textAlign="center"
            >
              Chat
            </Typography>

            <Grid item xs={3} position="absolute" right={1} marginBottom={1}>
              <FormControlLabel
                control={
                  <Switch
                    checked={value}
                    onChange={toggleTheme}
                    name="theme"
                    color="default"
                  />
                }
                name="theme"
                className="header-message"
                label={value ? "Dark Mode" : "Light Mode"}
                labelPlacement="start"
              />

              <Tooltip title="Account settings">
                <IconButton
                  onClick={handleClick}
                  size="small"
                  sx={{ ml: 2 }}
                  aria-controls={open ? "account-menu" : undefined}
                  aria-haspopup="true"
                  aria-expanded={open ? "true" : undefined}
                >
                  <Avatar sx={{ width: 32, height: 32 }}>
                    {username.charAt(0).toUpperCase()}
                  </Avatar>
                </IconButton>
              </Tooltip>

              <Menu
                anchorEl={anchorEl}
                id="account-menu"
                open={open}
                onClose={handleClose}
                onClick={handleClose}
                PaperProps={{
                  elevation: 0,
                  sx: {
                    overflow: "visible",
                    filter: "drop-shadow(0px 2px 8px rgba(0,0,0,0.32))",
                    mt: 1.5,
                    "& .MuiAvatar-root": {
                      width: 32,
                      height: 32,
                      ml: -0.5,
                      mr: 1,
                    },
                    "&:before": {
                      content: '""',
                      display: "block",
                      position: "absolute",
                      top: 0,
                      right: 14,
                      width: 10,
                      height: 10,
                      bgcolor: "background.paper",
                      transform: "translateY(-50%) rotate(45deg)",
                      zIndex: 0,
                    },
                  },
                }}
                transformOrigin={{ horizontal: "right", vertical: "top" }}
                anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
              >
                <MenuItem onClick={handleClose}>
                  <Avatar /> Account
                </MenuItem>
                <Divider />

                <MenuItem onClick={handleLogOut}>
                  <ListItemIcon>
                    <Logout fontSize="small" />
                  </ListItemIcon>
                  Logout
                </MenuItem>
              </Menu>
            </Grid>
          </Grid>
        </Grid>

        <Grid
          container
          component={Paper}
          className={classes.chatSection}
          bottom={0}
          onFocus={handleFocus}
        >
          {users.current.length > 0 ? (
            <ChatUsers
              username={username}
              classes={classes}
              setChatWith={setChatWith}
              websocket={websocket}
              users={users.current}
            />
          ) : null}

          {chatWith.length > 0 && chatWith !== username && chatWith !== null ? (
            <ChatArea
              classes={classes}
              username={username}
              chatWith={chatWith}
              websocket={websocket}
            />
          ) : null}
        </Grid>
      </>
    );
  }
}

import React, { useState } from "react";
import { SearchUser } from "../../utils/operations";
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";
import ListItemIcon from "@mui/material/ListItemIcon";
import Divider from "@mui/material/Divider";
import Avatar from "@mui/material/Avatar";
import Grid from "@mui/material/Grid";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";

import StarIcon from "@mui/icons-material/Star";
import AdjustIcon from "@mui/icons-material/Adjust";

export default function ChatUsers({
  username,
  classes,
  setChatWith,
  websocket,
  users,
}) {
  const [search, setSearch] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(-1);

  const handleListItemClick = (event, index) => {
    setSelectedIndex(index);
    websocket.current.send(
      JSON.stringify({
        from_author: username,
        to_author: users[index].USERNAME,
        command: "fetch_messages",
      })
    );
    setChatWith(users[index].USERNAME);
  };
  const handleSearch = async (event) => {
    setSearch(event.target.value);
    if (search.length > 1) {
      const searchUsers = await SearchUser(search);
      // setUsers([...searchUsers]);
    }
  };

  return (
    <Grid item xs={3} className={classes.borderRight500}>
      <List>
        <ListItem key={username}>
          <ListItemIcon>
            <Avatar
              alt={username}
              src="https://material-ui.com/static/images/avatar/1.jpg"
            />
          </ListItemIcon>
          <ListItemText primary={username.toUpperCase()}></ListItemText>
        </ListItem>
      </List>
      <Divider />
      <Grid item xs={12} style={{ padding: "10px" }}>
        <Autocomplete
          freeSolo
          id="search-users-field"
          options={users.map((option) => option.USERNAME)}
          renderInput={(params) => (
            <TextField
              id="outlined-basic-email"
              variant="outlined"
              fullWidth
              {...params}
              label="Search Users"
              InputProps={{
                ...params.InputProps,
                type: "search",
              }}
              value={search}
              onChange={handleSearch}
            />
          )}
        />
      </Grid>
      <Divider />
      <List>
        {users.map((user, index) => (
          <ListItemButton
            key={user.USERNAME}
            selected={selectedIndex === index}
            onClick={(event) => {
              handleListItemClick(event, index);
            }}
          >
            <ListItemIcon>
              <Avatar
                alt={user.USERNAME}
                src={
                  "https://material-ui.com/static/images/avatar/" +
                  (index + 2) +
                  ".jpg"
                }
              />
            </ListItemIcon>
            <ListItemText primary={user.USERNAME}>{user.USERNAME}</ListItemText>
            <ListItemText
              secondary={
                user.STAR ? (
                  <StarIcon color="primary" size="small" fontSize="10" />
                ) : null
              }
              align="right"
            ></ListItemText>
            <ListItemText
              secondary={
                user.IS_ACTIVE ? (
                  <AdjustIcon size="small" fontSize="4" color="success" />
                ) : null
              }
              align="right"
            ></ListItemText>
          </ListItemButton>
        ))}
      </List>
    </Grid>
  );
}

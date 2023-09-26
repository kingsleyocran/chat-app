import React, { useEffect, useState } from "react";
import Divider from "@mui/material/Divider";
import TextField from "@mui/material/TextField";
import SendIcon from "@mui/icons-material/Send";
import Grid from "@mui/material/Grid";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Fab from "@mui/material/Fab";

export default function ChatArea({ classes, username, chatWith, websocket }) {
  const [getData, setGetData] = useState([]);

  let inputMessage = React.createRef(null);
  const messageScroll = React.createRef(null);

  useEffect(() => {
    messageScroll.current?.scrollIntoView({ behavior: "smooth" });
  }, [messageScroll]);

  useEffect(() => {
    if (!websocket.current) return;

    //   // listen to messages from the socket
    websocket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data);

      if (
        data.type !== "start" &&
        data.command === "fetch_messages" &&
        data.issuer === username
      ) {
        setGetData([...data.message]);
      } else if (
        data.type === "chat_message" &&
        data.command === "new_message"
      ) {
        setGetData((prevState) => [...prevState, ...data.message]);
      } else if (data.command === null && data.issuer === username) {
        setGetData([]);
      }
      return () => {
        setGetData([]);
      };
    };
  }, [username, chatWith, websocket]);

  const handleSubmit = (e) => {
    e.preventDefault();

    const message = inputMessage.firstElementChild.control.value;

    // check if there is a message to send
    if (message.length >= 1) {
      // send the message to the socket
      websocket.current.send(
        JSON.stringify({
          messages: message,
          from_author: username,
          to_author: chatWith,
          command: "new_message",
        })
      );
    }

    // reset the message input field
    inputMessage.firstElementChild.control.value = "";
  };

  const messageBody = () => {
    return (
      <Grid item xs={9}>
        <List className={classes.messageArea}>
          {getData && getData.length >= 1
            ? getData.map((msg, index) => (
                <ListItem key={msg.id || index}>
                  <Grid container>
                    <Grid item xs={12}>
                      <ListItemText
                        align={msg.from_author === username ? "right" : "left"}
                        primary={msg.messages}
                        ref={
                          index + 1 === getData.length ? messageScroll : null
                        }
                      ></ListItemText>
                    </Grid>
                    <Grid item xs={12}>
                      <ListItemText
                        align={msg.from_author === username ? "right" : "left"}
                        secondary={new Date(
                          msg.created_at
                        ).toLocaleTimeString()}
                      ></ListItemText>
                    </Grid>
                  </Grid>
                </ListItem>
              ))
            : null}
        </List>
        <Divider />
        <Grid
          container
          component="form"
          onSubmit={(e) => handleSubmit(e)}
          style={{
            padding: "30px",
            marginTop: "20px",
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <Grid item xs={11}>
            <TextField
              id="send-message"
              label="Type Something"
              name="send-message"
              fullWidth
              type="text"
              ref={(e) => (inputMessage = e)}
            />
          </Grid>
          <Grid item xs={1} align="right">
            <Fab color="primary" aria-label="add">
              <SendIcon />
            </Fab>
          </Grid>
        </Grid>
      </Grid>
    );
  };
  return <>{messageBody()}</>;
}

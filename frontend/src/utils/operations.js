import { auth_request, chat_request } from "./request";
import { addItem, getItem, clearCache } from "./storage";
import {
  REGISTER_ROUTE,
  LOGIN_ROUTE,
  USERNAME_ROUTE,
  REFRESH_ROUTE,
  LOGOUT_ROUTE,
  ACCESS_TOKEN,
  REFRESH_TOKEN,
  SEARCH_USER_ROUTE,
  GET_ALL_USERS,
} from "../constants";
import AppSettings from "../config";

const headers = {
  "Content-Type": "application/json",
};

export async function registerUser(userDetails) {
  return await auth_request
    .post(
      REGISTER_ROUTE,
      {
        username: userDetails.username,
        email: userDetails.email,
        password: userDetails.password,
      },
      {
        headers: headers,
      }
    )
    .then(() => true)
    .catch((error) => {
      throw error.response.data;
    });
}

export async function logUserIn(userDetails) {
  await auth_request
    .post(
      LOGIN_ROUTE,
      {
        username: userDetails.username,
        password: userDetails.password,
      },
      {
        headers: headers,
      }
    )
    .then((response) => {
      const data = response.data;
      addItem(ACCESS_TOKEN, data?.access_token);
      addItem(REFRESH_TOKEN, data?.refresh_token);
    })
    .catch((error) => {
      const msg = error.response.data;
      throw msg;
    });
}

export async function getUsername() {
  const token = getItem(ACCESS_TOKEN);
  const refreshToken = getItem(REFRESH_TOKEN);
  if (refreshToken === null) {
    return null;
  }
  headers["Authorization"] = `Bearer ${token}`;

  return await auth_request
    .get(USERNAME_ROUTE, { headers: headers })
    .then((response) => response.data?.message)
    .catch(async () => {
      const success = await getNewAccessToken();
      if (success) {
        return await getUsername();
      } else {
        return null;
      }
    });
}

export async function getNewAccessToken() {
  const refreshToken = getItem(REFRESH_TOKEN);
  headers["Authorization"] = `Bearer ${refreshToken}`;

  return await fetch(AppSettings.authURL + REFRESH_ROUTE, {
    method: "POST",
    headers: headers,
  })
    .then(async (response) => {
      const data = await response.json();
      addItem(ACCESS_TOKEN, data?.access_token);
      addItem(REFRESH_TOKEN, data?.refresh_token);
      return true;
    })
    .catch((error) => {
      console.error(error);
      return false;
    });
}

export async function logOut() {
  const token = getItem(ACCESS_TOKEN);
  headers["Authorization"] = `Bearer ${token}`;
  fetch(AppSettings.authURL + LOGOUT_ROUTE, {
    method: "POST",
    headers: headers,
  })
    .then(async () => {
      clearCache();
    })
    .catch(async (error) => {
      console.error(error);
      const success = await getNewAccessToken();
      if (success) {
        await logOut();
      }
    });
}

export async function SearchUser(username) {
  return await chat_request
    .get(SEARCH_USER_ROUTE + username)
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      throw error?.response?.data;
    });
}

export async function getAllUsers() {
  return await chat_request
    .get(GET_ALL_USERS)
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      throw error?.response?.data;
    });
}

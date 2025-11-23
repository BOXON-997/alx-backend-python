
# Messaging App API – Postman Testing Guide

This README explains how to test the Messaging App API endpoints using Postman.

---

## 🔐 1. Authentication – Get JWT Token
**Endpoint:**  
`POST /api/token/`

**Body (JSON):**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
- `access` token
- `refresh` token

Use the `access` token for all authenticated requests.

---

## 💬 2. Create a Conversation  
**Endpoint:**  
`POST /api/chats/conversations/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body (JSON):**
```json
{
  "participants": [1, 2]
}
```

---

## ✉️ 3. Send a Message  
**Endpoint:**  
`POST /api/chats/messages/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body (JSON):**
```json
{
  "conversation": 1,
  "content": "Hello!"
}
```

---

## 📥 4. Fetch Conversations  
**Endpoint:**  
`GET /api/chats/conversations/`

**Headers:**
```
Authorization: Bearer <access_token>
```

---

## 🔒 5. Unauthorized Access Test
Try calling any endpoint **without** a token.

Expected result:
```
HTTP 401 Unauthorized
```

---

## 📄 Postman Collection
Import the file:

`post_man-Collections.json`

into Postman to run all tests automatically.

---

## ✔ Requirements Covered
- Creating conversations  
- Sending messages  
- Fetching conversations  
- JWT Authentication testing  
- Private conversation protection tests  


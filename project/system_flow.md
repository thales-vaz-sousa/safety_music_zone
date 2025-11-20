
### **1. Guest Interaction**

- **Step 1:** Guest opens the web app (mobile-friendly).
- **Step 2:** Guest searches for a song using a search bar.
- **Step 3:** Web app sends the search query to the backend.
- **Step 4:** Backend calls **Spotify API** to fetch:
    - Song title, artist, album.
    - Explicit flag.
- **Step 5:** If `explicit = true` → reject request with a message: _“Song contains explicit content.”_
- **Step 6:** If `explicit = false` → proceed to lyrics check.

---

### **2. Lyrics Analysis**

- **Step 7:** Backend calls **Lyrics API** (e.g., Musixmatch) to get lyrics.
- **Step 8:** Run **content filtering algorithm**:
    - Keyword-based profanity/sexual term detection.
    - Optional: NLP model for double-meaning detection.
- **Step 9:** If lyrics fail → reject request with message: _“Lyrics not appropriate.”_
- **Step 10:** If lyrics pass → add song to **pending queue**.

---

### **3. DJ Dashboard**

- **Step 11:** DJ logs in to the dashboard.
- **Step 12:** DJ sees:
    - Pending requests.
    - Song details (title, artist, explicit flag, lyrics status).
- **Step 13:** DJ approves or rejects the song.
- **Step 14:** Approved songs move to **play queue**.

---

### **4. Real-Time Updates**

- **Step 15:** Guests see:
    - Their request status (pending, approved, rejected).
    - Current playing song.
- **Step 16:** DJ can mark songs as “played” → updates guest view.

---

### **5. Optional Features**

- Voting system for guests.
- DJ can prioritize songs based on votes.
- Display “Top Requested Songs” on guest interface.
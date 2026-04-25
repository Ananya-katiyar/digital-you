const API_URL = import.meta.env.VITE_API_URL;

export async function fetchEmails(email) {
  const res = await fetch(`${API_URL}/emails/?email=${email}`);
  if (!res.ok) throw new Error("Failed to fetch emails");
  return res.json();
}

export async function fetchQueue(email) {
  const res = await fetch(`${API_URL}/queue/?email=${email}`);
  if (!res.ok) throw new Error("Failed to fetch queue");
  return res.json();
}

export async function fetchDecisions(email) {
  const res = await fetch(`${API_URL}/decisions/?email=${email}`);
  if (!res.ok) throw new Error("Failed to fetch decisions");
  return res.json();
}

export async function fetchProfile(email) {
  const res = await fetch(`${API_URL}/profile/?email=${email}`);
  if (!res.ok) throw new Error("Failed to fetch profile");
  return res.json();
}

export async function updateProfile(email, updates) {
  const res = await fetch(`${API_URL}/profile/?email=${email}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updates),
  });
  if (!res.ok) throw new Error("Failed to update profile");
  return res.json();
}

export async function approveQueueItem(emailId, userEmail) {
  const res = await fetch(
    `${API_URL}/queue/${emailId}/approve?user_email=${userEmail}`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error("Failed to approve item");
  return res.json();
}

export async function rejectQueueItem(emailId, userEmail) {
  const res = await fetch(
    `${API_URL}/queue/${emailId}/reject?user_email=${userEmail}`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error("Failed to reject item");
  return res.json();
}

export async function generateDraft(subject, snippet, tone, userEmail) {
  const res = await fetch(`${API_URL}/drafts/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      subject,
      snippet,
      tone,
      user_email: userEmail,
    }),
  });
  if (!res.ok) throw new Error("Failed to generate draft");
  return res.json();
}
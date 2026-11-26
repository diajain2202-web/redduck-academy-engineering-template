// 03-core-periphery/src/Store.ts  —  TYPESCRIPT version.
// Only edit this file if you chose TypeScript, and complete just one language.
// Then declare it at the top of SOLUTION.md:  language: "typescript"
//
// Given (do not edit): ./store-data holds the UserRecord type, the seed users,
// and the hash helper. Done for you: verify, which returns only a boolean.
// Your job:
//   - add a hash-free public-profile lookup that returns username and role,
//   - rebuild report so it lists every user without ever including a hash.
// Full description in TASK.md.

import { SEED_USERS, UserRecord, hash } from "./store-data";

export interface PublicProfile {
  username: string;
  role: string;
}

export interface UserDirectory {
  listUsernames(): string[];
  getPublicProfile(username: string): PublicProfile | undefined;
}

export class UserStore {
  #users: Record<string, UserRecord> = Object.fromEntries(
    Object.entries(SEED_USERS).map(([username, user]) => [username, { ...user }]),
  );

  // The one legitimate core operation. It checks a password and returns only a boolean.
  verify(username: string, password: string): boolean {
    const user = this.#users[username];
    if (!user) return false;
    return user.passwordHash === hash(password);
  }

  listUsernames(): string[] {
    return Object.keys(this.#users);
  }

  getPublicProfile(username: string): PublicProfile | undefined {
    const user = this.#users[username];
    if (!user) return undefined;
    return { username: user.username, role: user.role };
  }
}

// Periphery: build a report using only the core's hash-free directory interface.
export function reportUsers(directory: UserDirectory): PublicProfile[] {
  return directory.listUsernames().map((username) => {
    const profile = directory.getPublicProfile(username);
    if (!profile) {
      throw new Error(`User disappeared from directory: ${username}`);
    }
    return profile;
  });
}

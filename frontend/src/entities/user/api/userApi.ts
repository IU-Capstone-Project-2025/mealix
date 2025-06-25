import { UserProfile } from "../model/types";
import { apiPOST } from "@shared/lib/utils/api";

export interface SaveUserProfileResponse {
  success: boolean;
  data: UserProfile;
  message?: string;
}

export async function saveUserProfile(profile: UserProfile): Promise<SaveUserProfileResponse> {
  return apiPOST<UserProfile, SaveUserProfileResponse>('/user', profile);
}
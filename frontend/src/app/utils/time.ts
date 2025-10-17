/**
 * Converts uptime in hundredths of a second to a human-readable format (days, hours, minutes, seconds).
 * @param hundredths - Uptime in hundredths of a second.
 * @returns A formatted string representing the uptime.
 */
export const formatUptime = (hundredths: number): string => {
  const seconds = Math.floor(hundredths / 100);
  const days = Math.floor(seconds / 86400);
  const hrs = Math.floor((seconds % 86400) / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  return `${days}d ${hrs}h ${mins}m ${secs}s`;
};

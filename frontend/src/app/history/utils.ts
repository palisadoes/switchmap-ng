type DeviceNode = {
  idxDevice: number;
  hostname: string;
  sysName: string;
  zone?: string;
  lastPolled?: number | string | null;
  lastPolledMs?: number | null;
};

// Cache for device data
interface CacheEntry {
  data: DeviceNode[];
  timestamp: number;
}

export const deviceCache = new Map<string, CacheEntry>();


export function toMs(value: number | string | null | undefined): number | null {
  if (value == null) return null;
  if (typeof value === "number") return value < 1e12 ? value * 1000 : value;
  const ms = Date.parse(value);
  return Number.isNaN(ms) ? null : ms;
}

export function filterDevicesByTimeRange(
  devices: DeviceNode[],
  timeRange: string,
  start?: string,
  end?: string
): DeviceNode[] {
  const now = new Date();

  function parseDateOnlyLocal(yyyyMmDd: string): Date {
    const [y, m, d] = yyyyMmDd.split("-").map(Number);
    return new Date(y, (m ?? 1) - 1, d ?? 1);
  }

  if (timeRange === "custom" && start && end) {
    const startDate = parseDateOnlyLocal(start);
    startDate.setHours(0, 0, 0, 0);
    const endDate = parseDateOnlyLocal(end);
    endDate.setHours(23, 59, 59, 999);

    return devices.filter((d) => {
      if (typeof d.lastPolledMs !== "number") return false;
      const t = d.lastPolledMs;
      return t >= startDate.getTime() && t <= endDate.getTime();
    });
  }

  let startDate: Date | null = null;
  switch (timeRange) {
    case "1d":
      startDate = new Date(now);
      startDate.setDate(now.getDate() - 1);
      break;
    case "1w":
      startDate = new Date(now);
      startDate.setDate(now.getDate() - 7);
      break;
    case "1m":
      startDate = new Date(now);
      startDate.setMonth(now.getMonth() - 1);
      break;
    case "6m":
      startDate = new Date(now);
      startDate.setMonth(now.getMonth() - 6);
      break;
  }

  if (startDate) {
    const startMs = startDate.getTime();
    return devices.filter((d) => {
      if (typeof d.lastPolledMs !== "number") return false;
      return d.lastPolledMs >= startMs;
    });
  }

  return devices;
}

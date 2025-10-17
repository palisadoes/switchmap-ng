"use client";

import { ZoneEdge } from "@/app/types/graphql/GetZoneDevices";
import { useEffect, useState, useRef } from "react";
/**
 * ZoneDropdown component allows users to select a zone from a dropdown list.
 * It fetches the available zones from the API and manages the selected zone state.
 *
 * @remarks
 * This component is designed for client-side use only because it relies on
 * the `useEffect` hook for fetching data and managing state.
 * It also handles click events outside the dropdown to close it.
 *
 * @returns The rendered component.
 *
 * @see {@link Zone} for the structure of a zone.
 * @see {@link ZoneDropdownProps} for the props used by the component.
 * @see {@link useState} for managing the selected zone state.
 * @see {@link useEffect} for fetching zones and handling side effects.
 * @see {@link useRef} for managing the dropdown reference to handle outside clicks.
 */

type Zone = {
  tsCreated: string;
  name: string;
  idxZone: string;
  id: string;
};

type ZoneDropdownProps = {
  selectedZoneId: string | null;
  onChange: (zoneId: string) => void;
};

export function ZoneDropdown({ selectedZoneId, onChange }: ZoneDropdownProps) {
  const [zones, setZones] = useState<Zone[]>([]);
  const [open, setOpen] = useState<boolean>(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    const fetchZones = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(
          process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT ||
            "http://localhost:7000/switchmap/api/graphql",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              query: `{
              events(last: 1) {
                edges {
                  node {
                    zones {
                      edges {
                        node {
                          tsCreated
                          id
                          idxZone
                          name
                        }
                      }
                    }
                  }
                }
              }
            }`,
            }),
          }
        );

        if (!res.ok) throw new Error(`Network error: ${res.status}`);

        const json = await res.json();
        if (json.errors) throw new Error(json.errors[0].message);

        const rawZones =
          json?.data?.events?.edges?.[0]?.node?.zones?.edges?.map(
            (edge: ZoneEdge) => edge.node
          ) ?? [];

        if (active) setZones(rawZones);
      } catch (err) {
        if (active)
          setError(
            err instanceof Error ? err.message : "Failed to fetch zones"
          );
      } finally {
        if (active) setLoading(false);
      }
    };

    fetchZones();

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const selected =
    selectedZoneId === "all"
      ? { name: "All", idxZone: "all", id: "all", tsCreated: "" }
      : (selectedZoneId && zones.find((z) => z.id === selectedZoneId)) ||
        (zones.length > 0 ? zones[0] : undefined);

  useEffect(() => {
    if (zones.length > 0) {
      if (selectedZoneId === "all") return;
      const found = zones.find((z) => z.id === selectedZoneId);
      if (!found) {
        onChange(zones[0].id);
      }
    }
  }, [zones, selectedZoneId]);

  return (
    <div
      className="relative inline-block text-left rounded-md"
      ref={dropdownRef}
    >
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="inline-flex justify-between items-center bg-bg w-48 px-4 py-2 border border-gray-300 rounded-md shadow-sm outline"
      >
        {selected?.name || `Zone ${selected?.idxZone || ""}`}

        {loading && " (Loading...)"}
        {error && " (Error)"}
        <svg
          className={`ml-2 h-5 w-5 transition-transform duration-200 ${
            open ? "rotate-180" : ""
          }`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      <p className="text-sm text-gray-700 pt-2 text-right">
        {selected?.tsCreated || ""}
      </p>

      {open && (
        <>
          {error && (
            <div className="absolute bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mt-1 w-48 z-10">
              Error: {error}
            </div>
          )}
          <div
            data-testid="zone-dropdown-menu"
            className="absolute bg-bg mt-1 w-48 rounded-md shadow-lg border border-color z-10 max-h-60 overflow-auto"
          >
            {zones.map((zone) => (
              <button
                data-testid={`zone-button-${zone.id}`}
                key={zone.id}
                onClick={() => {
                  onChange(zone.id);
                  setOpen(false);
                }}
                className="block w-full text-left px-4 py-2 hover:bg-hover-bg focus:outline-none"
              >
                {zone.name || `Zone ${zone.idxZone}`}
              </button>
            ))}
            <button
              key="all"
              data-testid="zone-button-all"
              onClick={() => {
                onChange("all");
                setOpen(false);
              }}
              className="block w-full text-left px-4 py-2 hover:bg-hover-bg focus:outline-none"
            >
              All
            </button>
          </div>
        </>
      )}
    </div>
  );
}

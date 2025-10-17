"use client";

import React, { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { FiLayout, FiClock, FiSettings } from "react-icons/fi";
import { RxHamburgerMenu } from "react-icons/rx";
import { ThemeToggle } from "@/app/theme-toggle";
/**
 * Sidebar component provides navigation links and a theme toggle button.
 * It supports both large screens (desktop) and small screens (mobile).
 * It includes a hamburger menu for mobile view and a slide-in sidebar.
 *
 * @remarks
 * This component is designed for client-side use only because it relies on
 * the `useState` and `useEffect` hooks for managing state and handling events.
 * It also includes responsive design features to adapt to different screen sizes.
 * The sidebar contains links to the dashboard, history, and configuration pages,
 *
 * @returns The rendered sidebar component.
 *
 * @see {@link ThemeToggle} for the theme switching functionality.
 * @see {@link Link} for navigation links.
 * @see {@link useState} for managing the open/close state of the sidebar.
 * @see {@link useEffect} for handling side effects like closing the sidebar on outside clicks.
 * @see {@link FiLayout}, {@link FiClock}, {@link FiSettings}, {@link RxHamburgerMenu} for the icons used in the sidebar.
 *
 */

export function Sidebar() {
  const [open, setOpen] = useState<boolean>(false);
  const sidebarRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent): void => {
      const target = e.target as Node;
      if (sidebarRef.current && !sidebarRef.current.contains(target)) {
        setOpen(false);
      }
    };

    if (open) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [open]);

  const sidebarContent = (
    <nav className="space-y-6">
      <div className="flex flex-row items-center justify-between gap-1">
        <img
          src="/images/switchmap-logo-modified.svg"
          alt="logo"
          className="w-6 h-6"
        />

        <h2 className="text-xl font-semibold">Switchmap-NG</h2>
        <ThemeToggle />
      </div>

      <ul className="list-none space-y-4">
        <li>
          <Link
            href="/"
            className="flex items-center gap-2 font-medium hover:text-primary transition-colors"
          >
            <FiLayout className="icon" />
            <p>Dashboard</p>
          </Link>
          <ul className="pl-6 mt-2 space-y-1 text-sm text-muted-foreground">
            <li className="hover:text-primary">
              <Link href="/#network-topology" onClick={() => setOpen(false)}>
                Network Topology
              </Link>
            </li>
            <li className="hover:text-primary">
              <Link href="/#devices-overview" onClick={() => setOpen(false)}>
                Devices Overview
              </Link>
            </li>
          </ul>
        </li>
        <li>
          <Link
            href="/history"
            className="flex items-center gap-2 hover:text-primary"
            onClick={() => setOpen(false)}
          >
            <FiClock className="icon" />
            History
          </Link>
        </li>
        <li>
          <Link
            href="/config"
            className="flex items-center gap-2 hover:text-primary"
            onClick={() => setOpen(false)}
          >
            <FiSettings className="icon" />
            <span>Configuration</span>
          </Link>
        </li>
      </ul>
    </nav>
  );

  return (
    <>
      {/* Hamburger button */}
      <button
        className="p-3 text-2xl lg:hidden h-fit sticky top-4 left-4 z-50 border border-border rounded bg-[#081028] text-white"
        onClick={() => setOpen(true)}
        aria-label="Open sidebar"
      >
        <RxHamburgerMenu />
      </button>

      {/* Static sidebar for large screens */}
      <aside className="sidebar hidden lg:block fixed top-0 left-0 w-60 h-screen border-r border-border lg:p-4 flex-shrink-0">
        {sidebarContent}
      </aside>

      {/* Slide-in sidebar for small/medium screens */}
      {open && (
        <>
          <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" />
          <aside
            data-testid="slide-in-sidebar"
            ref={sidebarRef}
            className="sidebar fixed top-0 left-0 w-60 h-full border-r border-border z-50 p-4 shadow-md transition-transform transform lg:hidden"
          >
            {sidebarContent}
          </aside>
        </>
      )}
    </>
  );
}

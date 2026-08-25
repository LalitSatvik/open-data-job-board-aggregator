"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { motion } from "motion/react";
import { Briefcase, KanbanSquare, LogOut } from "lucide-react";
import { apiPost } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { SessionUser } from "@/lib/useSession";

const NAV_ITEMS = [
  { href: "/", label: "Job Board", icon: Briefcase },
  { href: "/tracker", label: "Tracker", icon: KanbanSquare },
];

function initials(user: SessionUser) {
  const source = user.name || user.email;
  return source
    .split(/\s+/)
    .map((part) => part[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

function NavLinks({ pathname, onNavigate }: { pathname: string; onNavigate?: () => void }) {
  return (
    <>
      {NAV_ITEMS.map((item) => {
        const isActive = pathname === item.href;
        return (
          <Link key={item.href} href={item.href} onClick={onNavigate} className="relative block">
            {isActive && (
              <motion.span
                layoutId="nav-active-pill"
                className="glass-pill-dark absolute inset-0 rounded-2xl"
                transition={{ type: "spring", stiffness: 380, damping: 32 }}
              />
            )}
            <span
              className={cn(
                "relative z-10 flex items-center gap-3 rounded-2xl px-3.5 py-2.5 text-sm font-medium transition-colors duration-200",
                isActive
                  ? "text-primary-foreground"
                  : "text-foreground/65 hover:text-foreground"
              )}
            >
              <item.icon className="size-4" />
              {item.label}
            </span>
          </Link>
        );
      })}
    </>
  );
}

export function AppShell({
  user,
  children,
}: {
  user: SessionUser;
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();

  async function handleSignOut() {
    try {
      await apiPost("/auth/logout");
    } catch (error) {
      console.error("Failed to sign out cleanly", error);
    } finally {
      router.replace("/login");
      router.refresh();
    }
  }

  return (
    <div className="mx-auto flex w-full max-w-[1400px] flex-1 flex-col gap-4 p-4 lg:flex-row lg:gap-6 lg:p-6">
      {/* Mobile top bar */}
      <div className="glass-panel flex items-center justify-between gap-2 rounded-2xl px-3 py-2.5 lg:hidden">
        <div className="flex items-center gap-2 font-heading text-sm font-semibold">
          <span className="glass-pill-dark flex size-8 items-center justify-center rounded-full text-primary-foreground">
            JB
          </span>
          Job Board
        </div>
        <nav className="flex items-center gap-1">
          <NavLinks pathname={pathname} />
        </nav>
        <Button variant="ghost" size="icon-sm" onClick={handleSignOut} aria-label="Sign out">
          <LogOut />
        </Button>
      </div>

      {/* Desktop sidebar */}
      <aside className="glass-panel sticky top-6 hidden h-[calc(100dvh-3rem)] w-60 shrink-0 flex-col justify-between rounded-3xl p-4 lg:flex">
        <div className="flex flex-col gap-6">
          <div className="flex items-center gap-2.5 px-1.5">
            <span className="glass-pill-dark flex size-9 items-center justify-center rounded-full font-heading text-sm font-semibold text-primary-foreground">
              JB
            </span>
            <div className="flex flex-col leading-tight">
              <span className="font-heading text-sm font-semibold">Open Data</span>
              <span className="text-xs text-muted-foreground">Job Board</span>
            </div>
          </div>
          <nav className="flex flex-col gap-1">
            <NavLinks pathname={pathname} />
          </nav>
        </div>

        <div className="glass-pill flex items-center gap-2.5 rounded-2xl p-2.5">
          <span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-navy/10 font-heading text-xs font-semibold text-navy">
            {initials(user)}
          </span>
          <div className="flex min-w-0 flex-1 flex-col leading-tight">
            <span className="truncate text-xs font-medium">{user.name || "Signed in"}</span>
            <span className="truncate text-[0.7rem] text-muted-foreground">{user.email}</span>
          </div>
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={handleSignOut}
            aria-label="Sign out"
            className="shrink-0"
          >
            <LogOut />
          </Button>
        </div>
      </aside>

      <motion.main
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
        className="flex min-w-0 flex-1 flex-col gap-6"
      >
        {children}
      </motion.main>
    </div>
  );
}

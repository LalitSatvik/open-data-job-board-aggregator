"use client";

import { motion } from "motion/react";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "";

  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4 py-10">
      <motion.div
        initial={{ opacity: 0, y: 18, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="relative w-full max-w-md overflow-hidden rounded-[2rem] p-10 text-center shadow-[0_30px_70px_-25px_rgba(22,49,68,0.55)]"
        style={{
          backgroundImage:
            "linear-gradient(155deg, #163144 0%, #1b405b 40%, #4f8b83 75%, #dff3eb 100%)",
        }}
      >
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            backgroundImage:
              "radial-gradient(circle at 26% 18%, rgba(255,255,255,0.28), transparent 55%)",
          }}
        />
        <div className="relative flex flex-col items-center gap-6">
          <span className="glass-pill flex size-14 items-center justify-center rounded-full font-heading text-xl font-semibold text-white">
            JB
          </span>
          <div className="flex flex-col items-center gap-2">
            <h1 className="font-heading text-3xl font-semibold tracking-tight text-white">
              Open Data Job Board
            </h1>
            <p className="text-sm text-white/80">
              Sign in to search open roles and track every application in
              one place.
            </p>
          </div>
          <Button asChild size="lg" variant="secondary">
            <a href={`${apiUrl}/auth/google/login`}>Sign in with Google</a>
          </Button>
        </div>
      </motion.div>
    </main>
  );
}

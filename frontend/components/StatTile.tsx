"use client";

import { motion } from "motion/react";
import type { LucideIcon } from "lucide-react";

export function StatTile({
  label,
  value,
  hint,
  icon: Icon,
  delay = 0,
}: {
  label: string;
  value: string | number;
  hint?: string;
  icon?: LucideIcon;
  delay?: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay, ease: "easeOut" }}
      whileHover={{ y: -3 }}
      className="glass-panel flex flex-col gap-1.5 rounded-2xl px-5 py-4"
    >
      <div className="flex items-center gap-1.5 text-xs font-medium tracking-wide text-muted-foreground uppercase">
        {Icon && <Icon className="size-3.5" />}
        {label}
      </div>
      <p className="font-heading text-2xl font-semibold text-foreground sm:text-3xl">
        {value}
      </p>
      {hint && <p className="text-xs text-muted-foreground">{hint}</p>}
    </motion.div>
  );
}

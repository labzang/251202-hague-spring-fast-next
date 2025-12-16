import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "secondary" | "outline"
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors",
        {
          "border-transparent bg-blue-600 text-white": variant === "default",
          "border-transparent bg-gray-100 text-gray-900": variant === "secondary",
          "text-gray-950": variant === "outline",
        },
        className
      )}
      {...props}
    />
  )
}

export { Badge }


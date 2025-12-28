
import * as React from "react"

const Card = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        className={`rounded-lg border bg-white dark:bg-gray-800 shadow-sm ${className || ""}`}
        {...props}
    />
))
Card.displayName = "Card"

export { Card }

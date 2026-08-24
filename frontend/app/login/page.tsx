import { Button } from "@/components/ui/button";

export default function LoginPage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "";

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 px-4">
      <div className="flex flex-col items-center gap-2 text-center">
        <h1 className="text-2xl font-semibold tracking-tight">
          Open Data Job Board
        </h1>
        <p className="text-sm text-muted-foreground">
          Sign in to search jobs and track your applications.
        </p>
      </div>
      <Button asChild size="lg">
        <a href={`${apiUrl}/auth/google/login`}>Sign in with Google</a>
      </Button>
    </main>
  );
}

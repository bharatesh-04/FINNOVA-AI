'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function SubscriptionsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-primary-text">Subscriptions</h1>

      <Card>
        <CardHeader>
          <CardTitle>Recurring Subscriptions</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-secondary-text">Manage and track your subscriptions here.</p>
        </CardContent>
      </Card>
    </div>
  );
}

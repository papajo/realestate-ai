"use client";

import { useState, useEffect } from "react";
import Link from 'next/link';
import { useAuth } from "@/hooks/useAuth";
import { Card } from "@/components/ui/card";
import { toast } from "react-hot-toast";

export default function ProfilePage() {
    const { user, login } = useAuth(); // Assume login updates user state, or we need a refresh
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        full_name: "",
        email: "",
        new_password: "",
        confirm_password: "",
    });

    useEffect(() => {
        if (user) {
            setFormData((prev) => ({
                ...prev,
                full_name: user.full_name || "",
                email: user.email || "",
            }));
        }
    }, [user]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (formData.new_password && formData.new_password !== formData.confirm_password) {
            toast.error("Passwords do not match");
            return;
        }

        setLoading(true);
        try {
            const token = localStorage.getItem("token");
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/me`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    full_name: formData.full_name,
                    email: formData.email,
                    password: formData.new_password || undefined,
                }),
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || "Failed to update profile");
            }

            const updatedUser = await res.json();
            toast.success("Profile updated successfully!");
            // Ideally update global auth state here. For now, we rely on page reload or nav update.
        } catch (error: any) {
            toast.error(error.message);
        } finally {
            setLoading(false);
        }
    };

    if (!user) {
        return <div className="p-8 text-center">Loading profile...</div>;
    }

    return (
        <div className="p-8 max-w-2xl mx-auto">
            <div className="mb-6">
                <Link href="/" className="text-sm text-blue-600 hover:underline">
                    &larr; Back to Dashboard
                </Link>
            </div>
            <h1 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">User Profile</h1>

            <Card className="p-6 bg-white dark:bg-gray-800 shadow-md rounded-xl">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            Full Name
                        </label>
                        <input
                            name="full_name"
                            type="text"
                            value={formData.full_name}
                            onChange={handleChange}
                            className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            Email Address
                        </label>
                        <input
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleChange}
                            className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        />
                    </div>

                    <div className="border-t pt-4 mt-6">
                        <h3 className="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-200">Change Password</h3>
                        <div className="space-y-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                    New Password
                                </label>
                                <input
                                    name="new_password"
                                    type="password"
                                    placeholder="Leave blank to keep current"
                                    value={formData.new_password}
                                    onChange={handleChange}
                                    className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                                />
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Confirm New Password
                                </label>
                                <input
                                    name="confirm_password"
                                    type="password"
                                    value={formData.confirm_password}
                                    onChange={handleChange}
                                    className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                                />
                            </div>
                        </div>
                    </div>

                    <div className="pt-4 flex justify-end">
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
                        >
                            {loading ? "Saving..." : "Save Changes"}
                        </button>
                    </div>
                </form>
            </Card>

            <div className="mt-8 text-sm text-gray-500">
                <p>Account ID: {user.id}</p>
                <p>Member since: {new Date(user.created_at || Date.now()).toLocaleDateString()}</p>
            </div>
        </div>
    );
}
